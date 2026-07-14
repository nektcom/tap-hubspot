from __future__ import annotations

from typing import Any, Iterable

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
from tap_hubspot.client import HubspotStream


class OwnersStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/owners#endpoint?spec=GET-/crm/v3/owners/
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "owners"
    path = "/owners"
    primary_keys = ["id"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    # Tracks whether we are currently fetching archived owners.
    _fetch_archived: bool = False

    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
            description="Unique identifier of the record.",
        ),
        th.Property(
            "email",
            th.StringType,
            description="Email address of the owner.",
        ),
        th.Property(
            "firstName",
            th.StringType,
            description="First name of the owner.",
        ),
        th.Property(
            "lastName",
            th.StringType,
            description="Last name of the owner.",
        ),
        th.Property(
            "userId",
            th.IntegerType,
            description="Identifier of the associated user.",
        ),
        th.Property(
            "createdAt",
            th.StringType,
            description="Timestamp when the record was created.",
        ),
        th.Property(
            "updatedAt",
            th.StringType,
            description="Timestamp when the record was last updated.",
        ),
        th.Property(
            "archived",
            th.BooleanType,
            description="Whether the record is archived.",
        ),
        th.Property(
            "teams",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "id",
                        th.StringType,
                        description="Unique identifier of the team.",
                    ),
                    th.Property(
                        "name",
                        th.StringType,
                        description="Name of the team.",
                    ),
                    th.Property(
                        "primary",
                        th.BooleanType,
                        description="Whether this is the owner's primary team.",
                    ),
                ),
            ),
            description="Teams the owner belongs to.",
        ),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        if self._fetch_archived:
            params["archived"] = "true"
        return params

    def request_records(self, context: dict | None) -> Iterable[dict]:
        """Fetch non-archived owners first, then archived owners."""
        self._fetch_archived = False
        yield from super().request_records(context)

        self._fetch_archived = True
        yield from super().request_records(context)
