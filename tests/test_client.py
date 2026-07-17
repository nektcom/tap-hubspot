"""Unit tests for HubSpot client stream helpers that don't require live API access."""
from __future__ import annotations

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
