from __future__ import annotations

from tap_hubspot.client import DynamicIncrementalHubspotStream


class DealStream(DynamicIncrementalHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/deals
    """

    name = "deals"
    path = "/objects/deals"
    incremental_path = "/objects/deals/search"
    primary_keys = ["id"]
    replication_key = "hs_lastmodifieddate"
    records_jsonpath = "$[results][*]"
    _legacy_config_object_name = "deal"

    @property
    def url_base(self) -> str:
        return "https://api.hubapi.com/crm/v3"
