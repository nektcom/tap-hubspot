from __future__ import annotations

from tap_hubspot.client import DynamicHubspotStream


class LineItemStream(DynamicHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/line-items
    """

    name = "line_items"
    path = "/objects/line_items"
    primary_keys = ["id"]
    records_jsonpath = "$[results][*]"

    @property
    def properties_path(self) -> str:
        return "line_items"

    @property
    def url_base(self) -> str:
        return "https://api.hubapi.com/crm/v3"
