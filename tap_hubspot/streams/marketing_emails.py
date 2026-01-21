from __future__ import annotations

import json
from decimal import Decimal

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
from nekt_singer_sdk.helpers import types
from tap_hubspot.client import HubspotIncrementalStream
from typing_extensions import override


class MarketingEmailStream(HubspotIncrementalStream):
    """
    https://developers.hubspot.com/docs/api/crm/email
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "marketing_emails"
    path = "/emails"
    primary_keys = ["id"]
    replication_key = "updatedAt"
    replication_key_filter = "updatedAfter"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("activeDomain", th.StringType),
        th.Property("allEmailCampaignIds", th.ArrayType(th.StringType)),
        th.Property("archived", th.BooleanType),
        th.Property("businessUnitId", th.StringType),
        th.Property("campaign", th.StringType),
        th.Property("campaignName", th.StringType),
        th.Property("campaignUtm", th.StringType),
        th.Property("clonedFrom", th.StringType),
        th.Property("content", th.StringType),
        th.Property("createdAt", th.StringType),
        th.Property("createdById", th.StringType),
        th.Property("emailCampaignGroupId", th.StringType),
        th.Property("emailTemplateMode", th.StringType),  # e.g. "DRAG_AND_DROP"
        th.Property(
            "from",
            th.ObjectType(
                th.Property("customReplyTo", th.StringType),
                th.Property("fromName", th.StringType),
                th.Property("replyTo", th.StringType),
            ),
        ),
        th.Property("isAb", th.BooleanType),
        th.Property("isPublished", th.BooleanType),
        th.Property("isTransactional", th.BooleanType),
        th.Property("jitterSendTime", th.BooleanType),
        th.Property("language", th.StringType),
        th.Property("name", th.StringType),
        th.Property("previewKey", th.StringType),
        th.Property("primaryEmailCampaignId", th.StringType),
        th.Property("publishDate", th.StringType),
        th.Property("publishedAt", th.StringType),
        th.Property("publishedByEmail", th.StringType),
        th.Property("publishedById", th.StringType),
        th.Property("publishedByName", th.StringType),
        th.Property("sendOnPublish", th.BooleanType),
        th.Property("state", th.StringType),
        th.Property(
            "stats",
            th.ObjectType(
                th.Property(
                    "counters",
                    th.ObjectType(
                        th.Property("bounce", th.IntegerType),
                        th.Property("click", th.IntegerType),
                        th.Property("contactslost", th.IntegerType),
                        th.Property("delivered", th.IntegerType),
                        th.Property("dropped", th.IntegerType),
                        th.Property("hardbounced", th.IntegerType),
                        th.Property("notsent", th.IntegerType),
                        th.Property("open", th.IntegerType),
                        th.Property("pending", th.IntegerType),
                        th.Property("reply", th.IntegerType),
                        th.Property("selected", th.IntegerType),
                        th.Property("sent", th.IntegerType),
                        th.Property("softbounced", th.IntegerType),
                        th.Property("spamreport", th.IntegerType),
                        th.Property("suppressed", th.IntegerType),
                        th.Property("unsubscribed", th.IntegerType),
                    ),
                ),
                th.Property(
                    "deviceBreakdown",
                    th.ObjectType(
                        th.Property(
                            "click_device_type",
                            th.ObjectType(
                                th.Property("computer", th.IntegerType),
                                th.Property("mobile", th.IntegerType),
                                th.Property("unknown", th.IntegerType),
                            ),
                        ),
                        th.Property(
                            "open_device_type",
                            th.ObjectType(
                                th.Property("computer", th.IntegerType),
                                th.Property("mobile", th.IntegerType),
                                th.Property("unknown", th.IntegerType),
                            ),
                        ),
                    ),
                ),
                th.Property("qualifierStats", th.ObjectType()),
                th.Property(
                    "ratios",
                    th.ObjectType(
                        th.Property("bounceratio", th.IntegerType),
                        th.Property("clickratio", th.IntegerType),
                        th.Property("clickthroughratio", th.IntegerType),
                        th.Property("contactslostratio", th.IntegerType),
                        th.Property("deliveredratio", th.IntegerType),
                        th.Property("hardbounceratio", th.IntegerType),
                        th.Property("notsentratio", th.IntegerType),
                        th.Property("openratio", th.IntegerType),
                        th.Property("pendingratio", th.IntegerType),
                        th.Property("replyratio", th.IntegerType),
                        th.Property("softbounceratio", th.IntegerType),
                        th.Property("spamreportratio", th.IntegerType),
                        th.Property("unsubscribedratio", th.IntegerType),
                    ),
                ),
            ),
        ),
        th.Property("subcategory", th.StringType),
        th.Property("subject", th.StringType),
        th.Property(
            "subscriptionDetails",
            th.ObjectType(
                th.Property("officeLocationId", th.StringType),
                th.Property("subscriptionId", th.StringType),
                th.Property("subscriptionName", th.StringType),
            ),
        ),
        th.Property(
            "to",
            th.ObjectType(
                th.Property(
                    "contactIds",
                    th.ObjectType(
                        th.Property("exclude", th.ArrayType(th.StringType)),
                        th.Property("include", th.ArrayType(th.StringType)),
                    ),
                ),
                th.Property(
                    "contactIlsLists",
                    th.ObjectType(
                        th.Property("exclude", th.ArrayType(th.StringType)),
                        th.Property("include", th.ArrayType(th.StringType)),
                    ),
                ),
                th.Property(
                    "contactLists",
                    th.ObjectType(
                        th.Property("exclude", th.ArrayType(th.StringType)),
                        th.Property("include", th.ArrayType(th.StringType)),
                    ),
                ),
                th.Property("suppressGraymail", th.BooleanType),
            ),
        ),
        th.Property("type", th.StringType),
        th.Property("updatedAt", th.StringType),
        th.Property("updatedById", th.StringType),
        th.Property(
            "webversion",
            th.ObjectType(
                th.Property("domain", th.StringType),
                th.Property("enabled", th.BooleanType),
                th.Property("isPageRedirected", th.BooleanType),
                th.Property("slug", th.StringType),
                th.Property("url", th.StringType),
            ),
        ),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/marketing/v3"

    @override
    def post_process(self, row: types.Record, context: types.Context | None = None) -> dict | None:
        if "content" in row and isinstance(row["content"], dict):
            row["content"] = json.dumps(row["content"], default=lambda o: float(o) if isinstance(o, Decimal) else None)
        return super().post_process(row, context)
