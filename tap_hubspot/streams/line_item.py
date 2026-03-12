from __future__ import annotations

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
from tap_hubspot.client import HubspotStream


class LineItemStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/line-items
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "line_items"
    path = "/objects/line_items"
    primary_keys = ["id"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
            description="Unique identifier of the record.",
        ),
        th.Property(
            "properties",
            th.ObjectType(
                th.Property(
                    "createdate",
                    th.StringType,
                    description="Timestamp when the record was created.",
                ),
                th.Property(
                    "hs_lastmodifieddate",
                    th.StringType,
                    description="Timestamp when the record was last updated.",
                ),
                th.Property(
                    "hs_product_id",
                    th.StringType,
                    description="Identifier of the associated product.",
                ),
                th.Property(
                    "hs_recurring_billing_period",
                    th.StringType,
                    description="Recurring billing period for the line item.",
                ),
                th.Property(
                    "name",
                    th.StringType,
                    description="Name of the record.",
                ),
                th.Property(
                    "price",
                    th.StringType,
                    description="Monetary value associated with the line item.",
                ),
                th.Property(
                    "quantity",
                    th.StringType,
                    description="Quantity of the line item.",
                ),
                th.Property(
                    "recurringbillingfrequency",
                    th.StringType,
                    description="Frequency of recurring billing.",
                ),
            ),
            description="Object containing the line item's custom properties.",
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
