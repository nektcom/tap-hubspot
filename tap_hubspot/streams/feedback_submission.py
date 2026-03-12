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
        th.Property(
            "id",
            th.StringType,
            description="Unique identifier of the record.",
        ),
        th.Property(
            "properties",
            th.ObjectType(
                th.Property(
                    "city",
                    th.StringType,
                    description="City from the feedback submission.",
                ),
                th.Property(
                    "createdDate",
                    th.StringType,
                    description="Timestamp when the record was created.",
                ),
                th.Property(
                    "domain",
                    th.StringType,
                    description="Domain associated with the submission.",
                ),
                th.Property(
                    "hs_lastmodifieddate",
                    th.StringType,
                    description="Timestamp when the record was last updated.",
                ),
                th.Property(
                    "industry",
                    th.StringType,
                    description="Industry from the feedback submission.",
                ),
                th.Property(
                    "name",
                    th.StringType,
                    description="Name of the record.",
                ),
                th.Property(
                    "phone",
                    th.StringType,
                    description="Phone number from the feedback submission.",
                ),
                th.Property(
                    "state",
                    th.StringType,
                    description="State or status from the feedback submission.",
                ),
            ),
            description="Object containing the feedback submission's custom properties.",
        ),
        th.Property(
            "createdAt",
            th.StringType,
            description="Timestamp when the record was created.",
        ),
        th.Property(
            "updatedAt",
            th.StringType,
            description="Timestamp when the record was last updated.",
        ),
        th.Property(
            "archived",
            th.BooleanType,
            description="Whether the record is archived.",
        ),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"
