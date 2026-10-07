from __future__ import annotations

from datetime import datetime, timezone
from http import HTTPStatus
from typing import Any, Iterable

import requests
from nekt_singer_sdk import typing as th
from nekt_singer_sdk.custom_logger import internal_logger, user_logger
from nekt_singer_sdk.helpers.types import Context, Record
from tap_hubspot.client import HubspotStream

MARKETING_EVENTS_SCOPE = "crm.objects.marketing_events.read"


class _MarketingEventsBaseStream(HubspotStream):
    """Base for the Marketing Events API streams.

    These streams need the `crm.objects.marketing_events.read` scope, which connections
    authorized before it was added to the Nekt HubSpot app do not have. HubSpot answers
    those with 403 (category MISSING_SCOPES): the stream is skipped with a warning instead
    of failing the whole run. 401 is left to the SDK and stays fatal.
    """

    records_jsonpath = "$[results][*]"
    page_size = 100  # HubSpot max for these endpoints

    _forbidden_warned = False

    @property
    def url_base(self) -> str:
        return "https://api.hubapi.com/marketing/v3"

    def validate_response(self, response: requests.Response) -> None:
        if response.status_code == HTTPStatus.FORBIDDEN:
            self._warn_forbidden(response)
            return
        super().validate_response(response)

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        if response.status_code == HTTPStatus.FORBIDDEN:
            return
        yield from super().parse_response(response)

    def _warn_forbidden(self, response: requests.Response) -> None:
        # Child streams hit this once per parent event; warn the customer only once.
        if not self._forbidden_warned:
            self._forbidden_warned = True
            user_logger.warning(
                f"No data was extracted for the '{self.name}' stream: this HubSpot connection "
                "was authorized without permission to read marketing events. To sync it, "
                "reconnect HubSpot (authorize the connection again)."
            )
        try:
            body = response.json()
        except ValueError:
            body = response.text[:500]
        internal_logger.warning(
            f"[{self.name}] 403 on {response.request.method} {response.request.path_url}; "
            f"stream yields no records (expected scope {MARKETING_EVENTS_SCOPE}). body={body}"
        )


class MarketingEventStream(_MarketingEventsBaseStream):
    """Marketing events (webinars, conferences, etc.) and their attendance counters.

    https://developers.hubspot.com/docs/api-reference/latest/marketing/marketing-events/guide

    The list endpoint has no updated-since filter, so this stream is full table.
    """

    name = "marketing_events"
    path = "/marketing-events"
    primary_keys = ["objectId"]

    schema = th.PropertiesList(
        th.Property(
            "objectId",
            th.StringType,
            description="Internal ID of the marketing event in HubSpot (its record ID).",
        ),
        th.Property(
            "eventName",
            th.StringType,
            description="Name of the marketing event.",
        ),
        th.Property(
            "eventType",
            th.StringType,
            description="Type of the marketing event (e.g. webinar, conference).",
        ),
        th.Property(
            "eventDescription",
            th.StringType,
            description="Description of the marketing event.",
        ),
        th.Property(
            "eventOrganizer",
            th.StringType,
            description="Name of the organizer of the marketing event.",
        ),
        th.Property(
            "eventUrl",
            th.StringType,
            description="URL in the external event application where the marketing event can be managed.",
        ),
        th.Property(
            "eventStatus",
            th.StringType,
            description="Status of the marketing event.",
        ),
        th.Property(
            "eventStatusV2",
            th.StringType,
            description="Status of the marketing event, in HubSpot's newer status format.",
        ),
        th.Property(
            "eventCancelled",
            th.BooleanType,
            description="Whether the marketing event has been cancelled.",
        ),
        th.Property(
            "eventCompleted",
            th.BooleanType,
            description="Whether the marketing event has been completed.",
        ),
        th.Property(
            "startDateTime",
            th.DateTimeType,
            description="Start date and time of the marketing event.",
        ),
        th.Property(
            "endDateTime",
            th.DateTimeType,
            description="End date and time of the marketing event.",
        ),
        th.Property(
            "registrants",
            th.IntegerType,
            description="Number of contacts currently registered for the marketing event.",
        ),
        th.Property(
            "attendees",
            th.IntegerType,
            description="Number of contacts who attended the marketing event.",
        ),
        th.Property(
            "cancellations",
            th.IntegerType,
            description="Number of contacts whose registration was cancelled.",
        ),
        th.Property(
            "noShows",
            th.IntegerType,
            description="Number of contacts who registered but did not attend.",
        ),
        th.Property(
            "externalEventId",
            th.StringType,
            description="ID of this marketing event in the external event application that created it.",
        ),
        th.Property(
            "appInfo",
            th.ObjectType(
                th.Property("id", th.StringType, description="ID of the application."),
                th.Property("name", th.StringType, description="Name of the application."),
            ),
            description="Application (integration) that created the marketing event.",
        ),
        th.Property(
            "customProperties",
            th.ArrayType(
                th.ObjectType(
                    th.Property("name", th.StringType, description="Name of the property in the CRM."),
                    th.Property("value", th.StringType, description="Value of the property in the CRM."),
                )
            ),
            description="Custom CRM properties of the marketing event.",
        ),
        th.Property(
            "createdAt",
            th.DateTimeType,
            description="Timestamp when the marketing event was created.",
        ),
        th.Property(
            "updatedAt",
            th.DateTimeType,
            description="Timestamp when the marketing event was last updated.",
        ),
    ).to_dict()

    def get_child_context(self, record: Record, context: Context | None) -> Context | None:
        return {"marketing_event_id": record["objectId"]}


class MarketingEventParticipationStream(_MarketingEventsBaseStream):
    """Participation of each contact in each marketing event (one row per contact per event).

    HubSpot keeps only the contact's current state for the event (registered, attended,
    cancelled or no-show), so this stream is full table.
    """

    name = "marketing_event_participations"
    path = "/marketing-events/participations/{marketing_event_id}/breakdown"
    primary_keys = ["marketing_event_id", "contact_id"]
    parent_stream_type = MarketingEventStream
    state_partitioning_keys = []

    schema = th.PropertiesList(
        th.Property(
            "marketing_event_id",
            th.StringType,
            description="Internal ID of the marketing event in HubSpot (objectId in marketing_events).",
        ),
        th.Property(
            "contact_id",
            th.StringType,
            description="Internal ID of the contact in HubSpot.",
        ),
        th.Property(
            "id",
            th.StringType,
            description="Identifier HubSpot returns for the participation record.",
        ),
        th.Property(
            "createdAt",
            th.DateTimeType,
            description="Timestamp when the participation record was created.",
        ),
        th.Property(
            "properties",
            th.ObjectType(
                th.Property(
                    "attendanceState",
                    th.StringType,
                    description="Current participation state: REGISTERED, ATTENDED, CANCELLED, NO_SHOW or EMPTY.",
                ),
                th.Property(
                    "occurredAt",
                    th.DateTimeType,
                    description="When the current participation state happened.",
                ),
                th.Property(
                    "attendanceDurationSeconds",
                    th.IntegerType,
                    description="How long the contact attended the event, in seconds.",
                ),
                th.Property(
                    "attendancePercentage",
                    th.StringType,
                    description="Attendance duration as a percentage of the event duration.",
                ),
            ),
            description="Participation details of the contact in the event.",
        ),
        th.Property(
            "associations",
            th.ObjectType(
                th.Property(
                    "contact",
                    th.ObjectType(
                        th.Property("contactId", th.StringType, description="Internal ID of the contact in HubSpot."),
                        th.Property("email", th.StringType, description="Email of the contact."),
                        th.Property("firstname", th.StringType, description="First name of the contact."),
                        th.Property("lastname", th.StringType, description="Last name of the contact."),
                    ),
                    description="Contact who participated in the event.",
                ),
                th.Property(
                    "marketingEvent",
                    th.ObjectType(
                        th.Property(
                            "marketingEventId",
                            th.StringType,
                            description="Internal ID of the marketing event in HubSpot.",
                        ),
                        th.Property("name", th.StringType, description="Name of the marketing event."),
                        th.Property(
                            "externalAccountId",
                            th.StringType,
                            description="Account ID of the marketing event in the external event application.",
                        ),
                        th.Property(
                            "externalEventId",
                            th.StringType,
                            description="ID of the marketing event in the external event application.",
                        ),
                    ),
                    description="Marketing event the participation belongs to.",
                ),
            ),
            description="Contact and marketing event of this participation.",
        ),
    ).to_dict()

    def post_process(self, row: dict, context: Context | None = None) -> dict | None:
        row["marketing_event_id"] = str(context["marketing_event_id"])
        row["contact_id"] = ((row.get("associations") or {}).get("contact") or {}).get("contactId")
        props = row.get("properties") or {}
        if "occurredAt" in props:
            props["occurredAt"] = _to_iso_datetime(props["occurredAt"])
        return row


def _to_iso_datetime(value: Any) -> str | None:
    """HubSpot's spec types occurredAt as epoch milliseconds, but its guide shows an ISO string."""
    if value is None or (isinstance(value, str) and not value.isdigit()):
        return value
    return datetime.fromtimestamp(int(value) / 1000, tz=timezone.utc).isoformat()
