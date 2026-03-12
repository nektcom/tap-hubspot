from __future__ import annotations

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
from tap_hubspot.client import HubspotStream


class DealPipelineStream(HubspotStream):
    """
    https://legacydocs.hubspot.com/docs/methods/deals/get-all-deals
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "deal_pipelines"
    path = "/pipelines/deals"
    primary_keys = ["createdAt"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = th.PropertiesList(
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
            "active",
            th.BooleanType,
            description="Whether the pipeline is active.",
        ),
        th.Property(
            "stages",
            th.ArrayType(
                th.ObjectType(
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
                        th.ObjectType(
                            th.Property(
                                "isClosed",
                                th.BooleanType,
                                description="Whether the stage represents a closed state.",
                            ),
                            th.Property(
                                "probability",
                                th.StringType,
                                description="Deal win probability for the stage.",
                            ),
                        ),
                        description="Stage metadata.",
                    ),
                    th.Property(
                        "stageId",
                        th.StringType,
                        description="Unique identifier of the stage.",
                    ),
                    th.Property(
                        "createdAt",
                        th.IntegerType,
                        description="Timestamp when the stage was created.",
                    ),
                    th.Property(
                        "updatedAt",
                        th.IntegerType,
                        description="Timestamp when the stage was last updated.",
                    ),
                    th.Property(
                        "active",
                        th.BooleanType,
                        description="Whether the stage is active.",
                    ),
                ),
            ),
            description="List of pipeline stages.",
        ),
        th.Property(
            "objectType",
            th.StringType,
            description="Type classification of the pipeline object.",
        ),
        th.Property(
            "objectTypeId",
            th.StringType,
            description="Identifier of the object type.",
        ),
        th.Property(
            "pipelineId",
            th.StringType,
            description="Unique identifier of the pipeline.",
        ),
        th.Property(
            "createdAt",
            th.IntegerType,
            description="Timestamp when the pipeline was created.",
        ),
        th.Property(
            "updatedAt",
            th.IntegerType,
            description="Timestamp when the pipeline was last updated.",
        ),
        th.Property(
            "default",
            th.BooleanType,
            description="Whether this is the default pipeline.",
        ),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm-pipelines/v1"
