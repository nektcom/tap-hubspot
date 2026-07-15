from __future__ import annotations

import json

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
from tap_hubspot.client import HubspotStream


class LeadPipelineStream(HubspotStream):
    """https://developers.hubspot.com/docs/api-reference/crm-pipelines-v3/guide"""

    name = "lead_pipelines"
    path = "/pipelines/leads"
    primary_keys = ["id"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
            description="Unique identifier of the pipeline.",
        ),
        th.Property(
            "label",
            th.StringType,
            description="Name of the pipeline.",
        ),
        th.Property(
            "displayOrder",
            th.IntegerType,
            description="Order in which the pipeline is displayed.",
        ),
        th.Property(
            "archived",
            th.BooleanType,
            description="Whether the pipeline is archived.",
        ),
        th.Property(
            "createdAt",
            th.DateTimeType,
            description="Timestamp when the pipeline was created.",
        ),
        th.Property(
            "updatedAt",
            th.DateTimeType,
            description="Timestamp when the pipeline was last updated.",
        ),
        th.Property(
            "stages",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "id",
                        th.StringType,
                        description="Unique identifier of the stage.",
                    ),
                    th.Property(
                        "label",
                        th.StringType,
                        description="Name of the stage.",
                    ),
                    th.Property(
                        "displayOrder",
                        th.IntegerType,
                        description="Order in which the stage is displayed.",
                    ),
                    th.Property(
                        "metadata",
                        th.StringType,
                        description="JSON-encoded stage metadata (keys vary).",
                    ),
                    th.Property(
                        "archived",
                        th.BooleanType,
                        description="Whether the stage is archived.",
                    ),
                    th.Property(
                        "createdAt",
                        th.DateTimeType,
                        description="Timestamp when the stage was created.",
                    ),
                    th.Property(
                        "updatedAt",
                        th.DateTimeType,
                        description="Timestamp when the stage was last updated.",
                    ),
                    th.Property(
                        "writePermissions",
                        th.StringType,
                        description="Permission level required to edit this stage.",
                    ),
                ),
            ),
            description="List of pipeline stages.",
        ),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """Leads pipelines use v3, unlike deals/tickets which use legacy v1."""
        return "https://api.hubapi.com/crm/v3"

    def post_process(self, row: dict, context: dict | None = None) -> dict:
        """Serialize each stage's metadata dict to a JSON string for the schema."""
        for stage in row.get("stages") or []:
            if isinstance(stage.get("metadata"), dict):
                stage["metadata"] = json.dumps(stage["metadata"])
        return row
