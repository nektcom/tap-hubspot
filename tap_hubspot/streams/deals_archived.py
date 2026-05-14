from __future__ import annotations

from functools import cached_property
from typing import Any

from nekt_singer_sdk import typing as th
from tap_hubspot.client import DynamicHubspotStream


class ArchivedDealStream(DynamicHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/deals
    Fetches archived deals via the list endpoint with archived=true.
    Full-table replication only (HubSpot's search API does not return archived records).
    """

    name = "deals_archived"
    path = "/objects/deals"
    primary_keys = ["id"]
    records_jsonpath = "$[results][*]"

    @cached_property
    def schema(self) -> dict:
        schema = super().schema
        extra = th.PropertiesList(
            th.Property(
                "archivedAt",
                th.DateTimeType,
                description="Timestamp when the record was archived.",
            ),
            th.Property(
                "url",
                th.StringType,
                description="API URL of the record.",
            ),
        )
        schema["properties"].update(extra.to_dict()["properties"])
        return schema

    @property
    def url_base(self) -> str:
        return "https://api.hubapi.com/crm/v3"

    @property
    def properties_path(self) -> str:
        return "deals"

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        params["archived"] = "true"
        return params
