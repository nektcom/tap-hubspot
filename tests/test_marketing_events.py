"""Offline tests for the marketing_events and marketing_event_participations streams."""
from __future__ import annotations

import json
from unittest.mock import MagicMock
from urllib.parse import parse_qs, urlparse

import pytest
import requests
from nekt_singer_sdk.exceptions import FatalAPIError

from tap_hubspot.streams import marketing_events as me_module
from tap_hubspot.streams.marketing_events import (
    MarketingEventParticipationStream,
    MarketingEventStream,
    _to_iso_datetime,
)
from tap_hubspot.tap import TapHubspot

MISSING_SCOPES_BODY = {
    "status": "error",
    "message": "This app hasn't been granted all required scopes to make this call.",
    "category": "MISSING_SCOPES",
    "errors": [
        {
            "message": "One or more of the following scopes are required.",
            "context": {"requiredGranularScopes": ["crm.objects.marketing_events.read"]},
        }
    ],
}


def _event(object_id: str) -> dict:
    return {
        "objectId": object_id,
        "eventName": f"Webinar {object_id}",
        "eventType": "WEBINAR",
        "eventOrganizer": "Nekt",
        "startDateTime": "2026-09-01T13:00:00Z",
        "endDateTime": "2026-09-01T14:00:00Z",
        "eventCancelled": False,
        "eventCompleted": True,
        "registrants": 3,
        "attendees": 2,
        "cancellations": 0,
        "noShows": 1,
        "customProperties": [{"name": "hs_event_source", "value": "zoom"}],
        "createdAt": "2026-08-01T10:00:00Z",
        "updatedAt": "2026-09-02T10:00:00Z",
    }


def _participation(event_id: str, contact_id: str, occurred_at) -> dict:
    return {
        "id": f"p-{event_id}-{contact_id}",
        "createdAt": "2026-08-15T10:00:00Z",
        "associations": {
            "contact": {"contactId": contact_id, "email": f"{contact_id}@example.com"},
            "marketingEvent": {"marketingEventId": event_id, "name": f"Webinar {event_id}"},
        },
        "properties": {
            "attendanceState": "ATTENDED",
            "occurredAt": occurred_at,
            "attendanceDurationSeconds": 3600,
            "attendancePercentage": "100",
        },
    }


def _response(request: requests.PreparedRequest, status: int, payload: dict) -> requests.Response:
    response = requests.Response()
    response.status_code = status
    response._content = json.dumps(payload).encode()
    response.headers["Content-Type"] = "application/json"
    response.url = request.url
    response.request = request
    return response


@pytest.fixture(autouse=True)
def block_network(monkeypatch):
    """Fail any test that would reach the network; `_route` replaces this with a fake."""

    def blocked(*args, **kwargs):
        raise AssertionError("network access is blocked in offline tests")

    monkeypatch.setattr(requests.Session, "send", blocked)
    monkeypatch.setattr(requests, "get", blocked)
    monkeypatch.setattr(requests, "post", blocked)


@pytest.fixture
def tap(monkeypatch):
    """A tap with only the marketing events streams and a private app token (no OAuth call)."""
    monkeypatch.setattr(
        TapHubspot,
        "discover_streams",
        lambda self: [MarketingEventStream(self), MarketingEventParticipationStream(self)],
    )
    return TapHubspot(
        config={"access_token": "fake-token", "start_date": "2026-01-01T00:00:00Z"},
        parse_env_config=False,
        validate_config=False,
    )


@pytest.fixture
def loggers(monkeypatch):
    user, internal = MagicMock(), MagicMock()
    monkeypatch.setattr(me_module, "user_logger", user)
    monkeypatch.setattr(me_module, "internal_logger", internal)
    return user, internal


def _route(monkeypatch, handler):
    """Serve every HTTP request from `handler(request)`; nothing reaches the network."""
    calls = []

    def fake_send(self, request, **kwargs):
        calls.append(request)
        return handler(request)

    monkeypatch.setattr(requests.Session, "send", fake_send)
    return calls


def test_marketing_events_paginates_and_builds_child_context(tap, monkeypatch, loggers):
    def handler(request):
        after = parse_qs(urlparse(request.url).query).get("after")
        if not after:
            return _response(request, 200, {"results": [_event("1")], "paging": {"next": {"after": "abc"}}})
        return _response(request, 200, {"results": [_event("2")]})

    calls = _route(monkeypatch, handler)
    stream = tap.streams["marketing_events"]

    records = list(stream.get_records(None))

    assert [r["objectId"] for r in records] == ["1", "2"]
    assert urlparse(calls[0].url).path == "/marketing/v3/marketing-events"
    assert parse_qs(urlparse(calls[0].url).query)["limit"] == ["100"]
    assert calls[0].headers["Authorization"] == "Bearer fake-token"
    assert stream.get_child_context(records[0], None) == {"marketing_event_id": "1"}
    loggers[0].warning.assert_not_called()


def test_participations_add_keys_and_normalize_occurred_at(tap, monkeypatch, loggers):
    def handler(request):
        assert urlparse(request.url).path == "/marketing/v3/marketing-events/participations/1/breakdown"
        return _response(
            request,
            200,
            {
                "total": 2,
                "results": [
                    _participation("1", "101", 1788264000000),
                    _participation("1", "102", "2026-09-01T13:05:00Z"),
                ],
            },
        )

    _route(monkeypatch, handler)
    stream = tap.streams["marketing_event_participations"]
    context = {"marketing_event_id": "1"}

    records = [stream.post_process(r, context) for r in stream.get_records(context)]

    assert [(r["marketing_event_id"], r["contact_id"]) for r in records] == [("1", "101"), ("1", "102")]
    assert records[0]["properties"]["occurredAt"] == "2026-09-01T12:00:00+00:00"
    assert records[1]["properties"]["occurredAt"] == "2026-09-01T13:05:00Z"
    assert stream.primary_keys == ["marketing_event_id", "contact_id"]


def _records_by_stream(stdout: str) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for line in stdout.splitlines():
        if line.startswith("{"):
            message = json.loads(line)
            if message["type"] == "RECORD":
                out.setdefault(message["stream"], []).append(message["record"])
    return out


def test_sync_all_emits_events_and_participations_per_event(tap, monkeypatch, loggers, capsys):
    def handler(request):
        path = urlparse(request.url).path
        if path == "/marketing/v3/marketing-events":
            return _response(request, 200, {"results": [_event("1"), _event("2")]})
        event_id = path.split("/")[-2]
        results = [_participation(event_id, f"{event_id}0{n}", 1788264000000) for n in (1, 2)]
        return _response(request, 200, {"total": 2, "results": results})

    calls = _route(monkeypatch, handler)

    tap.sync_all()

    records = _records_by_stream(capsys.readouterr().out)
    assert len(records["marketing_events"]) == 2
    assert sorted((r["marketing_event_id"], r["contact_id"]) for r in records["marketing_event_participations"]) == [
        ("1", "101"),
        ("1", "102"),
        ("2", "201"),
        ("2", "202"),
    ]
    assert len(calls) == 3  # 1 list + 1 breakdown per event
    loggers[0].warning.assert_not_called()


def test_missing_scope_skips_stream_without_failing(tap, monkeypatch, loggers):
    _route(monkeypatch, lambda request: _response(request, 403, MISSING_SCOPES_BODY))
    stream = tap.streams["marketing_events"]

    assert list(stream.get_records(None)) == []

    user, internal = loggers
    user.warning.assert_called_once()
    assert "reconnect HubSpot" in user.warning.call_args[0][0]
    internal.warning.assert_called_once()
    assert "MISSING_SCOPES" in internal.warning.call_args[0][0]


def test_missing_scope_on_child_warns_customer_once(tap, monkeypatch, loggers):
    _route(monkeypatch, lambda request: _response(request, 403, MISSING_SCOPES_BODY))
    stream = tap.streams["marketing_event_participations"]

    for event_id in ("1", "2", "3"):
        assert list(stream.get_records({"marketing_event_id": event_id})) == []

    user, internal = loggers
    user.warning.assert_called_once()
    assert internal.warning.call_count == 3


def test_unauthorized_stays_fatal(tap, monkeypatch, loggers):
    _route(monkeypatch, lambda request: _response(request, 401, {"status": "error", "category": "INVALID_AUTHENTICATION"}))
    stream = tap.streams["marketing_events"]

    with pytest.raises(FatalAPIError):
        list(stream.get_records(None))
    loggers[0].warning.assert_not_called()


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (None, None),
        (1788264000000, "2026-09-01T12:00:00+00:00"),
        ("1788264000000", "2026-09-01T12:00:00+00:00"),
        ("2026-09-01T13:05:00Z", "2026-09-01T13:05:00Z"),
    ],
)
def test_to_iso_datetime(value, expected):
    assert _to_iso_datetime(value) == expected
