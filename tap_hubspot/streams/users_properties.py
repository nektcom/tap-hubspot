from __future__ import annotations

from tap_hubspot.client import DynamicIncrementalHubspotStream


class UsersPropertiesStream(DynamicIncrementalHubspotStream):
    """CRM Users object (HubSpot object type "users", internal id 0-115).

    Distinct from the `users` stream, which reads the Settings API
    (/settings/v3/users) and only exposes id/email/roleIds/primaryteamid.
    This stream reads the CRM Users object and exposes its full property set
    (hs_given_name, hs_family_name, hs_email, hs_job_title, hubspot_owner_id,
    hs_deactivated, hs_searchable_calculated_name, etc.), the same way
    deals/companies/contacts/tasks do.

    Requires the `crm.objects.users.read` scope on the HubSpot private app,
    which is sensitive and must be granted explicitly by a Super Admin.
    Accounts/tokens without it are skipped at discovery time by
    `TapHubspot._safe_streams` (403 -> PermissionError -> stream omitted).

    https://developers.hubspot.com/docs/api/crm/understanding-the-crm
    """

    name = "users_properties"
    path = "/objects/users"
    incremental_path = "/objects/users/search"
    primary_keys = ["id"]
    replication_key = "hs_lastmodifieddate"
    records_jsonpath = "$[results][*]"

    @property
    def properties_path(self) -> str:
        return "users"

    @property
    def api_object_type(self) -> str:
        return "users"

    @property
    def url_base(self) -> str:
        return "https://api.hubapi.com/crm/v3"
