from __future__ import annotations

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
from tap_hubspot.client import HubspotStream


class GoalStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/goals
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "goals"
    path = "/objects/goal_targets"
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
                    "createdate",
                    th.StringType,
                    description="Timestamp when the record was created.",
                ),
                th.Property(
                    "hs_created_by_user_id",
                    th.StringType,
                    description="Identifier of the user who created the goal.",
                ),
                th.Property(
                    "hs_end_datetime",
                    th.StringType,
                    description="End date and time of the goal period.",
                ),
                th.Property(
                    "hs_goal_name",
                    th.StringType,
                    description="Name of the goal.",
                ),
                th.Property(
                    "hs_lastmodifieddate",
                    th.StringType,
                    description="Timestamp when the record was last updated.",
                ),
                th.Property(
                    "hs_start_datetime",
                    th.StringType,
                    description="Start date and time of the goal period.",
                ),
                th.Property(
                    "hs_target_amount",
                    th.StringType,
                    description="Target value or amount for the goal.",
                ),
            ),
            description="Object containing the goal's custom properties.",
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
