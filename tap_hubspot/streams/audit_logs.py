"""Audit Logs stream for tap-hubspot."""

from __future__ import annotations

from typing import Any, Generator

import pendulum
import requests
from nekt_singer_sdk import typing as th
from nekt_singer_sdk.custom_logger import user_logger
from nekt_singer_sdk.exceptions import FatalAPIError, RetriableAPIError
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

    # HubSpot rejects audit-log queries older than 365 days with a 400 error.
    # Stay a bit inside that window to avoid boundary/clock-skew issues.
    MAX_HISTORY_DAYS = 364

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
        # HubSpot only allows querying the last 365 days of audit logs and returns a
        # 400 for anything older. Clamp occurredAfter to the allowed window so an old
        # start date / bookmark doesn't crash the tap; we still pull the maximum
        # available history.
        min_allowed = pendulum.now("UTC").subtract(days=self.MAX_HISTORY_DAYS)
        starting_value = self.get_starting_replication_key_value(context)
        if starting_value:
            starting_dt = pendulum.parse(starting_value)
            if starting_dt < min_allowed:
                user_logger.warning(
                    "[audit_logs] Requested start date is older than HubSpot's "
                    f"365-day audit history limit; clamping occurredAfter to the last "
                    f"{self.MAX_HISTORY_DAYS} days."
                )
                starting_dt = min_allowed
        else:
            starting_dt = min_allowed
        params["occurredAfter"] = starting_dt.isoformat()
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
            if "older than 365 days" in str(e):
                user_logger.warning(
                    "audit_logs stream requested data older than HubSpot's 365-day audit "
                    "history limit. Skipping stream."
                )
                return
            raise
        except RetriableAPIError as e:
            if "500" in str(e):
                user_logger.warning(
                    f"audit_logs stream returned a 500 Internal Server Error from HubSpot. "
                    "This is a transient HubSpot-side error. Skipping stream."
                )
                return
            raise

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        row = super().post_process(row, context) or row
        # HubSpot returns actingUser.userId as an integer, but the schema declares it
        # as a string; coerce it so the record matches the column type. HubSpot may
        # also return actingUser as a bare user id instead of an object, so wrap it.
        acting_user = row.get("actingUser")
        if isinstance(acting_user, dict):
            for key in ("userId", "userEmail"):
                value = acting_user.get(key)
                if value is not None:
                    acting_user[key] = str(value)
        elif acting_user is not None:
            row["actingUser"] = {"userId": str(acting_user), "userEmail": None}
        return row
