"""REST client handling, including HubspotStream base class."""

from __future__ import annotations

import json
import re
import sys
import time
from functools import cached_property
from http import HTTPStatus
from typing import Any, Callable, Iterable

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


def uses_private_app_token(config: dict) -> bool:
    """Decide whether to authenticate with a static private app token (Bearer) vs OAuth.

    Selection is driven by the credentials actually present, so it stays correct even when
    the ``auth_mode`` selector is not propagated to the tap (e.g. not declared as a meltano
    setting, in which case ``auth_mode`` falls back to its ``"oauth"`` schema default): an
    ``access_token`` without an OAuth ``refresh_token`` means a private app token, while a
    ``refresh_token`` means OAuth. ``auth_mode`` is only used as a tiebreaker when neither
    credential is present.
    """
    has_oauth = "refresh_token" in config.get("oauth_credentials", {})
    has_token = bool(config.get("access_token"))
    if has_token and not has_oauth:
        return True
    if has_oauth:
        return False
    return config.get("auth_mode") == "private_app_token"


# Custom object type IDs follow the pattern "2-XXXXX" (e.g., "2-12345").
# These are not valid field names in most downstream systems, so we prefix them.
_CUSTOM_OBJECT_TYPE_ID_PATTERN = re.compile(r"^\d+-\d+$")


def sanitize_association_key(key: str, qualified_name_to_object_type_id: dict[str, str] | None = None) -> str:
    """Normalize an association key to a stable, downstream-safe field name.

    - Custom object type IDs (e.g. '2-12345') are prefixed with 'custom_' and have
      their hyphens replaced with underscores -> 'custom_2_12345'.
    - HubSpot returns associations keyed by the object's fullyQualifiedName
      (e.g. 'p44530090_clientes_rmapp'), which embeds the portal ID and is therefore
      account-specific. When a mapping from qualified name to objectTypeId is given,
      such keys are normalized back to the stable 'custom_<objectTypeId>' form.
    - The API may return association keys with spaces (e.g. 'line items' instead of
      'line_items'). Spaces are normalized to underscores.
    - Standard association names (e.g. 'contacts', 'companies') are returned as-is.
    """
    if qualified_name_to_object_type_id and key in qualified_name_to_object_type_id:
        object_type_id = qualified_name_to_object_type_id[key]
        return f"custom_{object_type_id.replace('-', '_')}"
    if _CUSTOM_OBJECT_TYPE_ID_PATTERN.match(key):
        return f"custom_{key.replace('-', '_')}"
    return key.replace(" ", "_")


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

        if uses_private_app_token(self.config):
            return BearerTokenAuthenticator(
                self,
                token=self.config.get("access_token"),
            )
        else:
            return HubSpotOAuthAuthenticator(
                self,
                auth_endpoint="https://api.hubapi.com/oauth/v1/token",
                default_expiration=1800,
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


class HubspotIncrementalStream(HubspotStream):

    replication_key_filter = None

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
        if self.replication_key and self.replication_key_filter:
            params[self.replication_key_filter] = self.get_starting_replication_key_value(context)
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
    def _properties_as_json_string(self) -> bool:
        return self.config.get("properties_as_json_string", False)

    @cached_property
    def schema(self) -> dict:
        """Return a draft JSON schema for this stream."""
        self.hs_properties = self._get_available_properties()

        if self._properties_as_json_string:
            properties_type = th.StringType
        else:
            hs_props = [th.Property(name, self._get_datatype(type)) for name, type in self.hs_properties.items()]
            properties_type = th.ObjectType(*hs_props)

        schema = th.PropertiesList(
            th.Property(
                "id",
                th.StringType,
                description="Unique identifier of the record.",
            ),
            th.Property(
                "properties",
                properties_type,
                description="Object containing the record's custom properties.",
            ),
            th.Property(
                "createdAt",
                th.DateTimeType,
                description="Timestamp when the record was created.",
            ),
            th.Property(
                "updatedAt",
                th.DateTimeType,
                description="Timestamp when the record was last updated.",
            ),
            th.Property(
                "archived",
                th.BooleanType,
                description="Whether the record is archived.",
            ),
        )
        return schema.to_dict()

    def post_process(
        self,
        row: dict,
        context: dict | None = None,
    ) -> dict | None:
        if self._properties_as_json_string and isinstance(row.get("properties"), dict):
            row["properties"] = json.dumps(row["properties"])
        return row

    def _get_available_properties(self) -> dict[str, str]:
        session = requests.Session()
        session.auth = self.authenticator

        resp = session.get(
            f"https://api.hubapi.com/crm/v3/properties/{self.properties_path}",
        )
        if resp.status_code == 403:
            raise PermissionError(
                f"Token lacks access to '{self.properties_path}' object type. "
                "Check the Private App Token scopes in HubSpot."
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

    # Override in subclasses that have legacy per-stream property-history config keys
    # (e.g. "deal" for extract_deal_property_history).
    _legacy_config_object_name: str | None = None

    # HubSpot property types that the CRM Search API (incremental_path) rejects with a
    # blanket 400 "There was a problem with the request" when included in the request
    # body's "properties" array (e.g. hs_origin_object_coordinates, added by HubSpot to
    # contacts/companies/calls/communications around 2026-07). These properties are still
    # available on the regular GET/full-table path, so they're only excluded here.
    _SEARCH_UNSUPPORTED_PROPERTY_TYPES = {"object_coordinates"}

    @property
    def _search_safe_properties(self) -> list[str]:
        return [
            name
            for name, prop_type in self.hs_properties.items()
            if prop_type not in self._SEARCH_UNSUPPORTED_PROPERTY_TYPES
        ]

    # HubSpot hard-caps /search request bodies at 3,000 characters. Leave a small
    # margin (the "after" token and epoch timestamps vary a little in length
    # across pages) without being so conservative that accounts comfortably under
    # the real limit get switched onto the batch/read path unnecessarily.
    _SEARCH_BODY_SAFE_LIMIT = 2900
    _BATCH_READ_CHUNK_SIZE = 100

    @cached_property
    def _use_lean_search_properties(self) -> bool:
        """Whether this stream's full /search body would risk HubSpot's 3,000-char cap.

        Measures a representative body (same shape prepare_request_payload builds:
        filters, sorts, pagination, and the full properties list) rather than just
        the properties list length, so streams with comfortable headroom are left
        on the existing single-call path unchanged.

        When over the limit, /search only requests the replication key (enough to
        find and page through matching records); full property values are
        hydrated afterward via /batch/read, which has no such body-size limit.
        """
        sample_body = {
            "after": "9999",
            "filters": [
                {"propertyName": self.replication_key, "operator": "GTE", "value": "9999999999999"},
                {"propertyName": "hs_object_id", "operator": "GTE", "value": "99999999999"},
            ],
            "sorts": [{"propertyName": "hs_object_id", "direction": "ASCENDING"}],
            "limit": 200,
            "properties": self._search_safe_properties,
        }
        return len(json.dumps(sample_body)) > self._SEARCH_BODY_SAFE_LIMIT

    @property
    def _search_request_properties(self) -> list[str]:
        """The "properties" value to send in the /search request body.

        Lean (just the replication key) when the full list would risk HubSpot's
        3,000-char /search body cap; the full safe property list otherwise, which
        is the unchanged behavior for the vast majority of streams/accounts.
        """
        if self._use_lean_search_properties:
            return [self.replication_key]
        return self._search_safe_properties

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def _requests_session(self) -> requests.Session:
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=10,
        )
        session.mount("https://", adapter)
        return session

    @property
    def api_object_type(self) -> str:
        """Object type identifier used in HubSpot API URLs.

        Standard streams return self.name (e.g. "deals").
        Custom objects should override this to return their object_type_id.
        """
        return self.name

    @cached_property
    def associations_string_list(self) -> list[str] | None:
        """Resolve the list of associations to extract for this stream from the unified config."""
        for entry in self.config.get("associations") or []:
            if entry.get("object_name") == self.name:
                value = entry.get("association_string", "")
                if value:
                    return value.replace(" ", "").split(",")
        return None

    @cached_property
    def should_extract_associations(self) -> bool:
        return bool(self.associations_string_list)

    @cached_property
    def property_history_string_list(self) -> list[str] | None:
        """Resolve property history list from legacy config. Returns None when not configured."""
        if not self._legacy_config_object_name:
            return None
        if not self.config.get(f"extract_{self._legacy_config_object_name}_property_history"):
            return None
        value = self.config.get(f"extract_{self._legacy_config_object_name}_property_history_comma_separated_string")
        if not value:
            return None
        return value.replace(" ", "").split(",")

    @cached_property
    def should_extract_property_history(self) -> bool:
        return bool(self.property_history_string_list)

    def _is_incremental_search(self, context):
        return self.replication_key and self.incremental_path is not None

    @cached_property
    def schema(self) -> dict:
        """Return a draft JSON schema for this stream."""
        self.hs_properties = self._get_available_properties()

        if self._properties_as_json_string:
            properties_type = th.StringType
        else:
            hs_props = [th.Property(name, self._get_datatype(type)) for name, type in self.hs_properties.items()]
            properties_type = th.ObjectType(*hs_props)

        schema = th.PropertiesList(
            th.Property(
                "id",
                th.StringType,
                description="Unique identifier of the record.",
            ),
            th.Property(
                "properties",
                properties_type,
                description="Object containing the record's custom properties.",
            ),
            th.Property(
                "createdAt",
                th.DateTimeType,
                description="Timestamp when the record was created.",
            ),
            th.Property(
                "updatedAt",
                th.DateTimeType,
                description="Timestamp when the record was last updated.",
            ),
            th.Property(
                "archived",
                th.BooleanType,
                description="Whether the record is archived.",
            ),
        )
        if self.replication_key:
            schema.append(
                th.Property(
                    self.replication_key,
                    th.DateTimeType,
                    description="Timestamp when the record was last updated.",
                )
            )
        schema_dict = schema.to_dict()

        if self.should_extract_associations:
            associations_schema = th.PropertiesList()
            for assoc in self.associations_string_list:
                associations_schema.append(
                    th.Property(
                        sanitize_association_key(assoc),
                        th.ArrayType(
                            th.ObjectType(
                                th.Property(
                                    "id", th.StringType, description="Unique identifier of the associated record."
                                ),
                                th.Property(
                                    "type", th.StringType, description="Type classification of the association."
                                ),
                            )
                        ),
                        description="List of associated records.",
                    )
                )
            schema_dict["properties"]["associations"] = associations_schema.to_dict()

        if self.should_extract_property_history:
            property_history_schema = th.PropertiesList()
            history_entry_type = th.ArrayType(
                th.ObjectType(
                    th.Property("sourceType", th.StringType, description="Type of the change source."),
                    th.Property("sourceId", th.StringType, description="Identifier of the change source."),
                    th.Property(
                        "updatedByUserId", th.IntegerType, description="Identifier of the user who made the change."
                    ),
                    th.Property("value", th.StringType, description="Value of the property at this change."),
                    th.Property("timestamp", th.StringType, description="Timestamp when the change occurred."),
                )
            )
            for prop_name in self.property_history_string_list:
                property_history_schema.append(
                    th.Property(prop_name, history_entry_type, description="History of changes for this property.")
                )
            schema_dict["properties"]["propertiesWithHistory"] = property_history_schema.to_dict()

        return schema_dict

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

        Handles fetching associations and property history via an additional API
        call when configured, then applies standard post-processing (replication
        key extraction, JSON-string conversion).
        """
        if self.should_extract_associations or self.should_extract_property_history:
            additional_data = self._fetch_additional_data_with_retry(
                self.api_object_type,
                row["id"],
                self.associations_string_list if self.should_extract_associations else None,
                self.property_history_string_list if self.should_extract_property_history else None,
            )
            if "associations" in additional_data:
                row["associations"] = additional_data["associations"]
            if "propertiesWithHistory" in additional_data:
                row["propertiesWithHistory"] = additional_data["propertiesWithHistory"]

        if self.replication_key:
            val = None
            if props := row.get("properties"):
                val = props[self.replication_key]
            row[self.replication_key] = val
        self.last_record_id = row.get("id")

        if self._properties_as_json_string and isinstance(row.get("properties"), dict):
            row["properties"] = json.dumps(row["properties"])

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
                    "properties": self._search_request_properties,
                }
            )

        return body

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        records = list(super().parse_response(response))
        if self._is_incremental_search(None) and self._use_lean_search_properties:
            records = self._hydrate_properties_via_batch_read(records)
        yield from records

    def _hydrate_properties_via_batch_read(self, records: list[dict]) -> list[dict]:
        """Fill in full property values for records fetched via a lean (ID-only) search.

        Used when the account has too many properties to fit them all in the
        /search request body. /batch/read has no such limit, so this fetches the
        full properties in chunks of up to 100 records instead.
        """
        records_by_id = {record["id"]: record for record in records}
        ids = list(records_by_id)

        for start in range(0, len(ids), self._BATCH_READ_CHUNK_SIZE):
            chunk = ids[start : start + self._BATCH_READ_CHUNK_SIZE]
            for result in self._batch_read_properties(chunk):
                record = records_by_id.get(result["id"])
                if record:
                    record["properties"] = result.get("properties", {})

        return list(records_by_id.values())

    def _batch_read_properties(self, ids: list[str]) -> list[dict]:
        """Fetch full property values for up to 100 record IDs via /batch/read, with retries."""
        batch_read_url = f"{self.url_base}/objects/{self.api_object_type}/batch/read"
        payload = {"inputs": [{"id": record_id} for record_id in ids], "properties": self._search_safe_properties}

        max_retries = 5
        for attempt in range(max_retries):
            headers = (
                self.authenticator.auth_headers
                if self.config.get("access_token")
                else {"Authorization": f"Bearer {self.authenticator.access_token}"}  # this ensures a token refresh
            )

            try:
                response = self._requests_session.post(batch_read_url, json=payload, headers=headers, timeout=30)
                response.raise_for_status()
                return response.json().get("results", [])

            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code
                is_last_attempt = attempt >= max_retries - 1

                if status_code == HTTPStatus.UNAUTHORIZED and not is_last_attempt:
                    user_logger.warning("Token expired while batch-reading properties, refreshing token and retrying.")
                    if hasattr(self.authenticator, "update_access_token"):
                        self.authenticator.update_access_token()
                    continue

                if (status_code == HTTPStatus.TOO_MANY_REQUESTS or status_code >= 500) and not is_last_attempt:
                    delay = self._retry_delay_seconds(e.response, attempt)
                    user_logger.warning(
                        f"HubSpot returned {status_code} batch-reading properties for {self.name}; "
                        f"retrying in {delay:.1f}s (attempt {attempt + 1}/{max_retries})."
                    )
                    time.sleep(delay)
                    continue

                raise

        return []

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
            headers = (
                self.authenticator.auth_headers
                if self.config.get("access_token")
                else {"Authorization": f"Bearer {self.authenticator.access_token}"}  # this ensures a token refresh
            )

            try:
                response = self._requests_session.get(details_url, params=params, headers=headers, timeout=30)
                response.raise_for_status()

                response_payload = response.json()
                associations_data = response_payload.get("associations", {})
                property_history_data = response_payload.get("propertiesWithHistory", {})
                qualified_name_to_object_type_id = getattr(
                    self._tap, "custom_object_qualified_name_to_object_type_id", None
                )
                return {
                    "associations": {
                        sanitize_association_key(k, qualified_name_to_object_type_id): v.get("results")
                        for k, v in associations_data.items()
                    },
                    "propertiesWithHistory": {k: v for k, v in property_history_data.items()},
                }

            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code
                is_last_attempt = attempt >= max_retries - 1

                if status_code == HTTPStatus.UNAUTHORIZED and not is_last_attempt:
                    user_logger.warning(
                        f"Token expired while fetching additional data for {object_type} {record_id}, refreshing token and retrying."
                    )
                    if hasattr(self.authenticator, "update_access_token"):
                        self.authenticator.update_access_token()
                    continue

                # 429 = HubSpot rate limit. Retry returning {} here would silently drop
                # associations/propertiesWithHistory for this record (e.g. deal 59827085596).
                # 5xx = transient server errors — also worth retrying.
                if (status_code == HTTPStatus.TOO_MANY_REQUESTS or status_code >= 500) and not is_last_attempt:
                    delay = self._retry_delay_seconds(e.response, attempt)
                    user_logger.warning(
                        f"HubSpot returned {status_code} fetching additional data for {object_type} {record_id}; "
                        f"retrying in {delay:.1f}s (attempt {attempt + 1}/{max_retries})."
                    )
                    time.sleep(delay)
                    continue

                user_logger.warning(f"Failed to fetch additional data for {object_type} {record_id}: {e}")
                return {}
            except requests.exceptions.RequestException as e:
                user_logger.warning(f"Failed to fetch additional data for {object_type} {record_id}: {e}")
                return {}

    @staticmethod
    def _retry_delay_seconds(response: requests.Response, attempt: int) -> float:
        """Honor HubSpot's Retry-After header when present; fall back to exponential backoff."""
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return max(float(retry_after), 1.0)
            except ValueError:
                pass
        # Exponential backoff: 2s, 4s, 8s, 16s
        return min(2 ** (attempt + 1), 30.0)
