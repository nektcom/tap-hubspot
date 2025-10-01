"""REST client handling, including HubspotStream base class."""

from __future__ import annotations

import datetime
import sys
from functools import cached_property
from http import HTTPStatus
from typing import Any, Callable

import pendulum
import requests
from nekt_singer_sdk import typing as th
from nekt_singer_sdk.authenticators import BearerTokenAuthenticator
from nekt_singer_sdk.custom_logger import user_logger
from nekt_singer_sdk.streams import RESTStream
from nekt_singer_sdk.streams.core import REPLICATION_FULL_TABLE
from ratelimit import limits, sleep_and_retry
from tap_hubspot.auth import HubSpotOAuthAuthenticator

if sys.version_info < (3, 11):
    from backports.datetime_fromisoformat import MonkeyPatch

    MonkeyPatch.patch_fromisoformat()

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]


class HubspotStream(RESTStream):
    """tap-hubspot stream class."""

    @property
    def url_base(self) -> str:
        """
        Returns base url
        """
        return "https://api.hubapi.com/"

    records_jsonpath = "$[*]"
    next_page_token_jsonpath = "$.paging.next.after"
    page_size = 100

    @cached_property
    def authenticator(self) -> _Auth:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """

        if "refresh_token" in self.config.get("oauth_credentials", {}):
            return HubSpotOAuthAuthenticator(
                self,
                auth_endpoint="https://api.hubapi.com/oauth/v1/token",
                default_expiration=1800,
            )
        else:
            return BearerTokenAuthenticator(
                self,
                token=self.config.get("access_token"),
            )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        params["limit"] = self.page_size
        if next_page_token:
            params["after"] = next_page_token
        return params


class DynamicHubspotStream(HubspotStream):
    """DynamicHubspotStream"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_datatype(self, data_type: str) -> th.JSONTypeHelper:
        # TODO: consider typing more precisely
        return th.StringType()

    @property
    def properties_path(self) -> str:
        return self.name

    @cached_property
    def schema(self) -> dict:
        """Return a draft JSON schema for this stream."""
        hs_props = []
        self.hs_properties = self._get_available_properties()
        for name, type in self.hs_properties.items():
            hs_props.append(th.Property(name, self._get_datatype(type)))
        schema = th.PropertiesList(
            th.Property("id", th.StringType),
            th.Property(
                "properties",
                th.ObjectType(*hs_props),
            ),
            th.Property("createdAt", th.DateTimeType),
            th.Property("updatedAt", th.DateTimeType),
            th.Property("archived", th.BooleanType),
        )
        return schema.to_dict()

    def _get_available_properties(self) -> dict[str, str]:
        session = requests.Session()
        session.auth = self.authenticator

        resp = session.get(
            f"https://api.hubapi.com/crm/v3/properties/{self.properties_path}",
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        return {prop["name"]: prop["type"] for prop in results}

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params = super().get_url_params(context, next_page_token)
        if self.hs_properties:
            params["properties"] = ",".join(self.hs_properties)
        return params


class DynamicIncrementalHubspotStream(DynamicHubspotStream):
    """DynamicIncrementalHubspotStream"""

    date_filter = None
    record_id_filter = None
    last_record_id = None
    incremental_path = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _is_incremental_search(self, context):
        return self.replication_key and self.incremental_path is not None

    @cached_property
    def schema(self) -> dict:
        """Return a draft JSON schema for this stream."""
        hs_props = []
        self.hs_properties = self._get_available_properties()
        for name, type in self.hs_properties.items():
            hs_props.append(th.Property(name, self._get_datatype(type)))
        schema = th.PropertiesList(
            th.Property("id", th.StringType),
            th.Property(
                "properties",
                th.ObjectType(*hs_props),
            ),
            th.Property("createdAt", th.DateTimeType),
            th.Property("updatedAt", th.DateTimeType),
            th.Property("archived", th.BooleanType),
        )
        if self.replication_key:
            schema.append(
                th.Property(
                    self.replication_key,
                    th.DateTimeType,
                )
            )
        return schema.to_dict()

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        if self._is_incremental_search(context):
            return {}
        return super().get_url_params(context, next_page_token)

    def post_process(
        self,
        row: dict,
        context: dict | None = None,  # noqa: ARG002
    ) -> dict | None:
        """As needed, append or transform raw data to match expected structure.
        Optional. This method gives developers an opportunity to "clean up" the results
        prior to returning records to the downstream tap - for instance: cleaning,
        renaming, or appending properties to the raw record result returned from the
        API.
        Developers may also return `None` from this method to filter out
        invalid or not-applicable records from the stream.
        Args:
            row: Individual record in the stream.
            context: Stream partition or context dictionary.
        Returns:
            The resulting record dict, or `None` if the record should be excluded.
        """

        if self.replication_key:
            val = None
            if props := row.get("properties"):
                val = props[self.replication_key]
            row[self.replication_key] = val
        self.last_record_id = row.get("id")
        return row

    def prepare_request(self, context: dict | None, next_page_token: Any | None) -> requests.PreparedRequest:
        if self._is_incremental_search(context):
            # Search endpoints use POST request
            self.path = self.incremental_path
            self.http_method = "POST"
        return super().prepare_request(context, next_page_token)

    def prepare_request_payload(self, context: dict | None, next_page_token: Any | None) -> dict | None:
        """Prepare the data payload for the REST API request.

        By default, no payload will be sent (return None).

        Developers may override this method if the API requires a custom payload along
        with the request. (This is generally not required for APIs which use the
        HTTP 'GET' method.)

        Args:
            context: Stream partition or context dictionary.
            next_page_token: Token, page number or any request argument to request the
                next page of data.
        """
        page_size = 200
        body = {}

        if self._is_incremental_search(context):
            # Only filter in case we have a value to filter on
            # https://developers.hubspot.com/docs/api/crm/search
            if self.date_filter is None:
                starting_timestamp = self.get_starting_replication_key_value(context)
                if starting_timestamp and self.replication_method != REPLICATION_FULL_TABLE:
                    self.date_filter = pendulum.parse(starting_timestamp)
                    user_logger.info(
                        f"[{self.name}] Starting incremental sync using search endpoint with timestamp: {self.date_filter.isoformat()}"
                    )
                elif self.config.get("start_date"):
                    start_date = self.config.get("start_date")
                    self.date_filter = pendulum.parse(start_date)
                    user_logger.info(
                        f"[{self.name}] Starting full table sync using search endpoint with start date: {self.date_filter.isoformat()}"
                    )

            if next_page_token:
                # Hubspot wont return more than 10k records so when we hit 10k we
                # need to reset our epoch to most recent and not send the next_page_token
                if int(next_page_token) + page_size >= 10_000:
                    user_logger.warning(
                        f'More than 10k objects in the search result. Updating record_id filter to "{self.last_record_id}" and date filter to "{self.date_filter.isoformat()}".'
                    )
                    self.record_id_filter = {
                        "propertyName": "hs_object_id",
                        "operator": "GTE",
                        "value": self.last_record_id,
                    }
                else:
                    body["after"] = next_page_token

            epoch_ts = str(int(self.date_filter.timestamp() * 1000))

            filters = [
                {
                    "propertyName": self.replication_key,
                    "operator": "GTE",
                    "value": epoch_ts,
                }
            ]
            if self.record_id_filter:
                filters.append(self.record_id_filter)

            body.update(
                {
                    "filters": filters,
                    "sorts": [
                        {
                            "propertyName": "hs_object_id",
                            "direction": "ASCENDING",
                        }
                    ],
                    "limit": page_size,  # Hubspot sets a limit of most 200 per request. Default is 10
                    "properties": list(self.hs_properties),
                }
            )

        return body

    @sleep_and_retry
    @limits(calls=100, period=10)  # 100 calls per 10 seconds (HubSpot API limit)
    def _fetch_additional_data_with_retry(
        self,
        object_type: str,
        record_id: str,
        associations_list: list[str] = None,
        property_history_list: list[str] = None,
    ) -> dict:
        """Fetch additional data for a single record with retry logic."""
        details_url = f"{self.url_base}/objects/{object_type}/{record_id}"
        params = {}
        if associations_list:
            params["associations"] = associations_list
        if property_history_list:
            params["propertiesWithHistory"] = property_history_list

        max_retries = 5
        for attempt in range(max_retries):
            headers = self.authenticator.auth_headers

            try:
                response = requests.get(details_url, params=params, headers=headers, timeout=30)
                response.raise_for_status()

                response_payload = response.json()
                associations_data = response_payload.get("associations", {})
                property_history_data = response_payload.get("propertiesWithHistory", {})
                return {
                    "associations": {k: v.get("results") for k, v in associations_data.items()},
                    "propertiesWithHistory": {k: v for k, v in property_history_data.items()},
                }

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == HTTPStatus.UNAUTHORIZED and attempt < max_retries - 1:
                    user_logger.warning(
                        f"Token expired while fetching additional data for {object_type} {record_id}, refreshing token and retrying."
                    )
                    if hasattr(self.authenticator, "update_access_token"):
                        self.authenticator.update_access_token()
                    continue
                user_logger.warning(f"Failed to fetch additional data for {object_type} {record_id}: {e}")
                return {}
            except requests.exceptions.RequestException as e:
                user_logger.warning(f"Failed to fetch additional data for {object_type} {record_id}: {e}")
                return {}
