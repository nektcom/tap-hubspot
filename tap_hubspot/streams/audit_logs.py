"""Audit Logs stream for tap-hubspot."""

from __future__ import annotations

from typing import Any, Generator

import requests
from nekt_singer_sdk import typing as th
from nekt_singer_sdk.custom_logger import user_logger
from singer_sdk.exceptions import FatalAPIError
from tap_hubspot.client import HubspotStream

PropertiesList = th.PropertiesList
Property = th.Property
ObjectType = th.ObjectType
DateTimeType = th.DateTimeType
StringType = th.StringType


class AuditLogsStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api-reference/account-audit-logs-v3/guide

    Extracts audit log entries from the HubSpot Account Activity API.
    Tracks user actions such as CRM object creation, property updates,
    security activity, and more.

    Requires 'account-info.security.read' scope (Enterprise accounts only).
    """

    name = "audit_logs"
    path = "/activity/audit-logs"
    primary_keys = ["id"]
    replication_key = "occurredAt"
    records_jsonpath = "$[results][*]"

    schema = PropertiesList(
        Property(
            "id",
            StringType,
            description="Unique identifier of the audit log entry.",
        ),
        Property(
            "category",
            StringType,
            description="Category of the audit event (e.g. PIPELINE, PROPERTY_VALUE, CRITICAL_ACTION).",
        ),
        Property(
            "subCategory",
            StringType,
            description="Sub-category of the audit event (e.g. DEAL, CONTACT).",
        ),
        Property(
            "action",
            StringType,
            description="Action performed (e.g. UPDATE, PERFORM, CREATE).",
        ),
        Property(
            "targetObjectId",
            StringType,
            description="ID of the object that was acted upon.",
        ),
        Property(
            "occurredAt",
            DateTimeType,
            description="Timestamp when the audit event occurred.",
        ),
        Property(
            "actingUser",
            ObjectType(
                Property(
                    "userId",
                    StringType,
                    description="ID of the user who performed the action.",
                ),
                Property(
                    "userEmail",
                    StringType,
                    description="Email of the user who performed the action.",
                ),
            ),
            description="User who performed the audited action.",
        ),
    ).to_dict()

    @property
    def url_base(self) -> str:
        return "https://api.hubapi.com/account-info/v3"

    def get_url_params(self, context, next_page_token):
        params = super().get_url_params(context, next_page_token)
        starting_value = self.get_starting_replication_key_value(context)
        if starting_value:
            params["occurredAfter"] = starting_value
        return params

    def get_records(self, context: dict | None) -> Generator[dict, Any, None]:
        try:
            yield from super().get_records(context)
        except FatalAPIError as e:
            if "403" in str(e) or "MISSING_SCOPES" in str(e):
                user_logger.warning(
                    "audit_logs stream is not available: missing 'account-info.security.read' scope. "
                    "This scope requires a HubSpot Enterprise account and re-authorization of the OAuth connection. "
                    "Skipping stream."
                )
                return
            raise
