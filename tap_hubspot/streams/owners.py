from __future__ import annotations

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
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"
