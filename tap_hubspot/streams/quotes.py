from __future__ import annotations

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
from tap_hubspot.client import HubspotStream


class QuoteStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/quotes
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "quotes"
    path = "/objects/quotes"
    primary_keys = ["id"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property(
            "properties",
            th.ObjectType(
                th.Property("hs_createdate", th.StringType),
                th.Property("hs_expiration_date", th.StringType),
                th.Property("hs_quote_amount", th.StringType),
                th.Property("hs_quote_number", th.StringType),
                th.Property("hs_status", th.StringType),
                th.Property("hs_terms", th.StringType),
                th.Property("hs_title", th.StringType),
                th.Property("hubspot_owner_id", th.StringType),
            ),
        ),
        th.Property("createdAt", th.StringType),
        th.Property("updatedAt", th.StringType),
        th.Property("archived", th.BooleanType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"
