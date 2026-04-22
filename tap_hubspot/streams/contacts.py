from __future__ import annotations

from tap_hubspot.client import DynamicIncrementalHubspotStream


class ContactStream(DynamicIncrementalHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/contacts
    """

    name = "contacts"
    path = "/objects/contacts"
    incremental_path = "/objects/contacts/search"
    primary_keys = ["id"]
    replication_key = "lastmodifieddate"
    records_jsonpath = "$[results][*]"
    _legacy_config_object_name = "contact"

    @property
    def url_base(self) -> str:
        return "https://api.hubapi.com/crm/v3"
