"""Unit tests for HubSpot client stream helpers that don't require live API access."""
from __future__ import annotations

import json

import requests

from tap_hubspot.client import DynamicIncrementalHubspotStream


def test_search_safe_properties_excludes_unsupported_types():
    """HubSpot's CRM Search API 400s if "properties" includes types like
    "object_coordinates" (e.g. hs_origin_object_coordinates). Those properties should be
    dropped from the search payload while everything else is kept.
    """
    stream = object.__new__(DynamicIncrementalHubspotStream)
    stream.hs_properties = {
        "email": "string",
        "hs_origin_object_coordinates": "object_coordinates",
        "createdate": "datetime",
    }

    assert stream._search_safe_properties == ["email", "createdate"]


def test_search_safe_properties_keeps_all_when_no_unsupported_types():
    stream = object.__new__(DynamicIncrementalHubspotStream)
    stream.hs_properties = {"email": "string", "createdate": "datetime"}

    assert stream._search_safe_properties == ["email", "createdate"]


def _stream_with_n_properties(n: int, name_len: int = 20) -> DynamicIncrementalHubspotStream:
    stream = object.__new__(DynamicIncrementalHubspotStream)
    stream.replication_key = "lastmodifieddate"
    stream.hs_properties = {f"hs_property_{i:03d}".ljust(name_len, "x"): "string" for i in range(n)}
    return stream


def test_use_lean_search_properties_false_for_typical_small_account():
    """Most existing streams (calls, communications, companies, and small/medium
    contacts accounts) sit comfortably under HubSpot's 3,000-char /search body
    limit and must keep behaving exactly as before — no unnecessary extra API
    calls for accounts that were never at risk."""
    stream = _stream_with_n_properties(80)

    assert stream._use_lean_search_properties is False


def test_use_lean_search_properties_false_right_below_the_real_hubspot_limit():
    """Regression guard: the threshold must not be so conservative that accounts
    with real headroom under HubSpot's 3,000-char cap get switched over anyway."""
    stream = _stream_with_n_properties(100)

    assert stream._use_lean_search_properties is False


def test_use_lean_search_properties_true_once_body_would_exceed_hubspot_limit():
    """Heavily-customized accounts (contacts is the typical case — often hundreds
    of properties) push the /search body over HubSpot's 3,000-char cap; this must
    flip to the batch/read fallback before HubSpot ever rejects the request."""
    stream = _stream_with_n_properties(150)

    assert stream._use_lean_search_properties is True


def test_use_lean_search_properties_true_for_many_properties():
    stream = _stream_with_n_properties(500)

    assert stream._use_lean_search_properties is True


def test_search_request_properties_unchanged_for_typical_small_account():
    """Direct regression guard on the exact value sent as "properties" in the
    /search body: small accounts must keep getting the full property list, byte
    for byte, exactly as before this fix."""
    stream = _stream_with_n_properties(80)

    assert stream._search_request_properties == stream._search_safe_properties
    assert stream._search_request_properties != [stream.replication_key]


def test_search_request_properties_lean_for_large_account():
    stream = _stream_with_n_properties(150)

    assert stream._search_request_properties == [stream.replication_key]


def _fake_response(records: list[dict]) -> requests.Response:
    response = requests.Response()
    response.status_code = 200
    response._content = json.dumps(records).encode()
    return response


def test_parse_response_does_not_hydrate_for_typical_small_account(monkeypatch):
    """Critical regression guard: for the vast majority of streams/accounts (few
    properties), parse_response must behave exactly as before this fix — no extra
    /batch/read calls, records passed through unchanged."""
    stream = _stream_with_n_properties(80)
    stream.incremental_path = "/objects/contacts/search"
    stream.records_jsonpath = "$[*]"

    def fail_if_called(self, records):
        raise AssertionError("batch/read hydration must not run for small, unaffected accounts")

    monkeypatch.setattr(DynamicIncrementalHubspotStream, "_hydrate_properties_via_batch_read", fail_if_called)

    raw_records = [{"id": "1", "properties": {"lastmodifieddate": "1"}}]
    parsed = list(stream.parse_response(_fake_response(raw_records)))

    assert parsed == raw_records


def test_parse_response_hydrates_for_large_account(monkeypatch):
    stream = _stream_with_n_properties(150)
    stream.incremental_path = "/objects/contacts/search"
    stream.records_jsonpath = "$[*]"

    def fake_hydrate(self, records):
        for record in records:
            record["properties"]["email"] = "hydrated@example.com"
        return records

    monkeypatch.setattr(DynamicIncrementalHubspotStream, "_hydrate_properties_via_batch_read", fake_hydrate)

    raw_records = [{"id": "1", "properties": {"lastmodifieddate": "1"}}]
    parsed = list(stream.parse_response(_fake_response(raw_records)))

    assert parsed[0]["properties"]["email"] == "hydrated@example.com"


def test_hydrate_properties_via_batch_read_chunks_by_100_and_merges_results(monkeypatch):
    stream = object.__new__(DynamicIncrementalHubspotStream)
    calls = []

    def fake_batch_read_properties(self, ids):
        calls.append(list(ids))
        return [{"id": record_id, "properties": {"email": f"user{record_id}@example.com"}} for record_id in ids]

    monkeypatch.setattr(DynamicIncrementalHubspotStream, "_batch_read_properties", fake_batch_read_properties)

    records = [{"id": str(i), "properties": {"lastmodifieddate": "123"}} for i in range(150)]
    hydrated = stream._hydrate_properties_via_batch_read(records)

    assert [len(chunk) for chunk in calls] == [100, 50]
    assert len(hydrated) == 150
    hydrated_by_id = {record["id"]: record for record in hydrated}
    assert hydrated_by_id["0"]["properties"] == {"email": "user0@example.com"}
    assert hydrated_by_id["149"]["properties"] == {"email": "user149@example.com"}
