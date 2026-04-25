from __future__ import annotations

from tap_hubspot.client import DynamicIncrementalHubspotStream


class LeadsStream(DynamicIncrementalHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/leads
    """

    name = "leads"
    path = "/objects/leads"
    incremental_path = "/objects/leads/search"
    primary_keys = ["id"]
    replication_key = "hs_lastmodifieddate"
    records_jsonpath = "$[results][*]"
    _legacy_config_object_name = "lead"

    @property
    def url_base(self) -> str:
        return "https://api.hubapi.com/crm/v3"
