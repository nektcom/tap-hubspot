from __future__ import annotations

from functools import cached_property
from typing import Any, Iterable

import requests as req
from nekt_singer_sdk import typing as th
from nekt_singer_sdk.custom_logger import user_logger
from tap_hubspot.client import DynamicHubspotStream

# Max properties to include in the GET URL to avoid 414 URI Too Long errors.
# Conservative limit: ~150 properties * ~30 chars avg = ~4500 chars, well within typical limits.
_MAX_URL_PROPERTIES = 150


class ArchivedTaskStream(DynamicHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/tasks
    Fetches archived tasks via the list endpoint with archived=true.
    Full-table replication only (HubSpot's search API does not return archived records).
    """

    name = "tasks_archived"
    path = "/objects/tasks"
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
        return "tasks"

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        params["limit"] = self.page_size
        if next_page_token:
            params["after"] = next_page_token
        params["archived"] = "true"
        if self.hs_properties:
            props = list(self.hs_properties.keys())
            params["properties"] = ",".join(props[:_MAX_URL_PROPERTIES])
        return params

    def _batch_read_properties(
        self,
        record_ids: list[str],
        properties: list[str],
    ) -> dict[str, dict]:
        """Fetch properties for a batch of records via the POST batch read endpoint."""
        url = f"{self.url_base}/objects/tasks/batch/read?archived=true"
        headers = (
            self.authenticator.auth_headers
            if self.config.get("access_token")
            else {"Authorization": f"Bearer {self.authenticator.access_token}"}
        )
        results: dict[str, dict] = {}
        for i in range(0, len(properties), _MAX_URL_PROPERTIES):
            chunk = properties[i : i + _MAX_URL_PROPERTIES]
            body = {
                "properties": chunk,
                "inputs": [{"id": rid} for rid in record_ids],
            }
            resp = req.post(url, json=body, headers=headers, timeout=30)
            resp.raise_for_status()
            for item in resp.json().get("results", []):
                item_id = item["id"]
                if item_id not in results:
                    results[item_id] = {}
                results[item_id].update(item.get("properties", {}))
        return results

    def request_records(self, context: dict | None) -> Iterable[dict]:
        all_props = list(self.hs_properties.keys()) if self.hs_properties else []
        remaining_props = all_props[_MAX_URL_PROPERTIES:]

        if not remaining_props:
            yield from super().request_records(context)
            return

        user_logger.info(
            f"[{self.name}] {len(all_props)} properties detected, "
            f"fetching in chunks to avoid URI length limits."
        )

        buffer: list[dict] = []
        for record in super().request_records(context):
            buffer.append(record)
            if len(buffer) >= self.page_size:
                self._enrich_with_remaining_props(buffer, remaining_props)
                yield from buffer
                buffer = []

        if buffer:
            self._enrich_with_remaining_props(buffer, remaining_props)
            yield from buffer

    def _enrich_with_remaining_props(
        self,
        records: list[dict],
        remaining_props: list[str],
    ) -> None:
        """Merge remaining properties into buffered records via batch read."""
        record_ids = [r["id"] for r in records if r.get("id")]
        if not record_ids:
            return
        extra = self._batch_read_properties(record_ids, remaining_props)
        for record in records:
            rid = record.get("id")
            if rid and rid in extra:
                props = record.get("properties")
                if isinstance(props, dict):
                    props.update(extra[rid])
