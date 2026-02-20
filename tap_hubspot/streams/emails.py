from __future__ import annotations

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
from tap_hubspot.client import DynamicIncrementalHubspotStream


class EmailStream(DynamicIncrementalHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/email
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "emails"
    path = "/objects/emails"
    primary_keys = ["id"]
    incremental_path = "/objects/emails/search"
    replication_key = "hs_lastmodifieddate"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    def validate_response(self, response: requests.Response) -> None:
        return super().validate_response(response)

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"
