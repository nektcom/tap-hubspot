from __future__ import annotations

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
from tap_hubspot.client import HubspotStream


class EmailSubscriptionStream(HubspotStream):
    """
    https://legacydocs.hubspot.com/docs/methods/email/get_subscriptions
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = id keys for replication
    records_jsonpath = json response body
    """

    name = "email_subscriptions"
    path = "/subscriptions"
    primary_keys = ["id"]
    records_jsonpath = "$[subscriptionDefinitions][*]"  # Or override `parse_response`.

    schema = th.PropertiesList(
        th.Property(
            "id",
            th.IntegerType,
            description="Unique identifier of the record.",
        ),
        th.Property(
            "portalId",
            th.IntegerType,
            description="Identifier of the associated portal.",
        ),
        th.Property(
            "name",
            th.StringType,
            description="Name of the record.",
        ),
        th.Property(
            "description",
            th.StringType,
            description="Description of the email subscription.",
        ),
        th.Property(
            "active",
            th.BooleanType,
            description="Whether the subscription type is active.",
        ),
        th.Property(
            "internal",
            th.BooleanType,
            description="Whether the subscription is for internal use only.",
        ),
        th.Property(
            "category",
            th.StringType,
            description="Category classification of the subscription.",
        ),
        th.Property(
            "channel",
            th.StringType,
            description="Channel associated with the subscription.",
        ),
        th.Property(
            "internalName",
            th.StringType,
            description="Internal name of the subscription.",
        ),
        th.Property(
            "businessUnitId",
            th.IntegerType,
            description="Identifier of the associated business unit.",
        ),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/email/public/v1"
