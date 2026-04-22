from __future__ import annotations

from tap_hubspot.client import DynamicIncrementalHubspotStream


class CompanyStream(DynamicIncrementalHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/companies
    """

    name = "companies"
    path = "/objects/companies"
    incremental_path = "/objects/companies/search"
    primary_keys = ["id"]
    replication_key = "hs_lastmodifieddate"
    records_jsonpath = "$[results][*]"
    _legacy_config_object_name = "company"

    @property
    def url_base(self) -> str:
        return "https://api.hubapi.com/crm/v3"
