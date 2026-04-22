from __future__ import annotations

from os import PathLike
from typing import Any

from nekt_singer_sdk.singerlib.schema import Schema
from nekt_singer_sdk.tap_base import Tap
from tap_hubspot.client import DynamicIncrementalHubspotStream


class CustomObjectStream(DynamicIncrementalHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/crm-custom-objects
    """

    def __init__(
        self,
        tap: Tap,
        object_name: str,
        object_qualified_name: str,
        object_type_id: str,
        schema: str | PathLike | dict[str, Any] | Schema | None = None,
        *args,
        **kwargs,
    ) -> None:
        self.object_name = object_name
        self.object_type_id = object_type_id
        self.object_qualified_name = object_qualified_name
        super().__init__(tap, schema, *args, **kwargs)

    @property
    def name(self) -> str:
        return f"{self.object_name}"

    @property
    def path(self) -> str:
        # Use the private attribute if it's been set, otherwise compute the value
        if hasattr(self, "_path"):
            return self._path
        return f"/objects/{self.object_type_id}"

    @path.setter
    def path(self, value: str) -> None:
        # Allow parent classes to set the path for incremental searches
        # Store the value in a private attribute
        self._path = value

    @property
    def properties_path(self) -> str:
        return self.object_qualified_name

    @property
    def incremental_path(self) -> str:
        return f"/objects/{self.object_type_id}/search"

    primary_keys = ["id"]
    replication_key = "hs_lastmodifieddate"
    records_jsonpath = "$.results[*]"

    @property
    def api_object_type(self) -> str:
        """Custom objects use object_type_id (e.g. '2-12345') in API URLs."""
        return self.object_type_id

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"
