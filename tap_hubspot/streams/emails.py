from __future__ import annotations

from tap_hubspot.client import DynamicIncrementalHubspotStream


class EmailStream(DynamicIncrementalHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/email
    """

    name = "emails"
    path = "/objects/emails"
    incremental_path = "/objects/emails/search"
    primary_keys = ["id"]
    replication_key = "hs_lastmodifieddate"
    records_jsonpath = "$[results][*]"
    _legacy_config_object_name = "email"

    @property
    def url_base(self) -> str:
        return "https://api.hubapi.com/crm/v3"
