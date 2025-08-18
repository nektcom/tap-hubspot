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
        th.Property("id", th.IntegerType),
        th.Property("portalId", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("internal", th.BooleanType),
        th.Property("category", th.StringType),
        th.Property("channel", th.StringType),
        th.Property("internalName", th.StringType),
        th.Property("businessUnitId", th.IntegerType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/email/public/v1"
