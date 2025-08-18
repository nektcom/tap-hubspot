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
        th.Property("label", th.StringType),
        th.Property("displayOrder", th.IntegerType),
        th.Property("active", th.BooleanType),
        th.Property(
            "stages",
            th.ArrayType(
                th.ObjectType(
                    th.Property("label", th.StringType),
                    th.Property("displayOrder", th.IntegerType),
                    th.Property(
                        "metadata",
                        th.ObjectType(
                            th.Property("isClosed", th.BooleanType),
                            th.Property("probability", th.StringType),
                        ),
                    ),
                    th.Property("stageId", th.StringType),
                    th.Property("createdAt", th.IntegerType),
                    th.Property("updatedAt", th.IntegerType),
                    th.Property("active", th.BooleanType),
                ),
            ),
        ),
        th.Property("objectType", th.StringType),
        th.Property("objectTypeId", th.StringType),
        th.Property("pipelineId", th.StringType),
        th.Property("createdAt", th.IntegerType),
        th.Property("updatedAt", th.IntegerType),
        th.Property("default", th.BooleanType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm-pipelines/v1"
