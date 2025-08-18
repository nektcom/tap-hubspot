from __future__ import annotations

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
from tap_hubspot.client import HubspotStream


class EmailStream(HubspotStream):
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
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property(
            "properties",
            th.ObjectType(
                th.Property("createdate", th.StringType),
                th.Property("hs_email_direction", th.StringType),
                th.Property("hs_email_sender_email", th.StringType),
                th.Property("hs_email_sender_firstname", th.StringType),
                th.Property("hs_email_sender_lastname", th.StringType),
                th.Property("hs_email_status", th.StringType),
                th.Property("hs_email_subject", th.StringType),
                th.Property("hs_email_text", th.StringType),
                th.Property("hs_email_to_email", th.StringType),
                th.Property("hs_email_to_firstname", th.StringType),
                th.Property("hs_email_to_lastname", th.StringType),
                th.Property("hs_lastmodifieddate", th.StringType),
                th.Property("hs_timestamp", th.StringType),
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
