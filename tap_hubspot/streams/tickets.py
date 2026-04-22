from __future__ import annotations

from tap_hubspot.client import DynamicIncrementalHubspotStream


class TicketStream(DynamicIncrementalHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/tickets
    """

    name = "tickets"
    path = "/objects/tickets"
    incremental_path = "/objects/tickets/search"
    primary_keys = ["id"]
    replication_key = "hs_lastmodifieddate"
    records_jsonpath = "$[results][*]"
    _legacy_config_object_name = "ticket"

    @property
    def url_base(self) -> str:
        return "https://api.hubapi.com/crm/v3"
