from __future__ import annotations

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
from tap_hubspot.client import HubspotStream


class FeedbackSubmissionsStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/feedback-submissions
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "feedback_submissions"
    path = "/objects/feedback_submissions"
    primary_keys = ["id"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property(
            "properties",
            th.ObjectType(
                th.Property("city", th.StringType),
                th.Property("createdDate", th.StringType),
                th.Property("domain", th.StringType),
                th.Property("hs_lastmodifieddate", th.StringType),
                th.Property("industry", th.StringType),
                th.Property("name", th.StringType),
                th.Property("phone", th.StringType),
                th.Property("state", th.StringType),
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
