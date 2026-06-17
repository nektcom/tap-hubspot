from __future__ import annotations

from tap_hubspot.client import DynamicIncrementalHubspotStream


class ServiceStream(DynamicIncrementalHubspotStream):
    """
    HubSpot "Services" standard object (objectTypeId 0-162).

    https://developers.hubspot.com/docs/guides/crm/using-object-apis
    """

    name = "services"
    path = "/objects/services"
    incremental_path = "/objects/services/search"
    primary_keys = ["id"]
    replication_key = "hs_lastmodifieddate"
    records_jsonpath = "$[results][*]"

    @property
    def url_base(self) -> str:
        return "https://api.hubapi.com/crm/v3"
