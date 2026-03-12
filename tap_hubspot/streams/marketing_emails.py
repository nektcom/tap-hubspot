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
        th.Property(
            "id",
            th.StringType,
            description="Unique identifier of the record.",
        ),
        th.Property(
            "activeDomain",
            th.StringType,
            description="Domain used for the marketing email.",
        ),
        th.Property(
            "allEmailCampaignIds",
            th.ArrayType(th.StringType),
            description="List of campaign identifiers associated with the email.",
        ),
        th.Property(
            "archived",
            th.BooleanType,
            description="Whether the record is archived.",
        ),
        th.Property(
            "businessUnitId",
            th.StringType,
            description="Identifier of the associated business unit.",
        ),
        th.Property(
            "campaign",
            th.StringType,
            description="Identifier of the associated campaign.",
        ),
        th.Property(
            "campaignName",
            th.StringType,
            description="Name of the campaign.",
        ),
        th.Property(
            "campaignUtm",
            th.StringType,
            description="UTM parameters for the campaign.",
        ),
        th.Property(
            "clonedFrom",
            th.StringType,
            description="Identifier of the email this was cloned from.",
        ),
        th.Property(
            "content",
            th.StringType,
            description="HTML or structured content of the email.",
        ),
        th.Property(
            "createdAt",
            th.StringType,
            description="Timestamp when the record was created.",
        ),
        th.Property(
            "createdById",
            th.StringType,
            description="Identifier of the user who created the email.",
        ),
        th.Property(
            "emailCampaignGroupId",
            th.StringType,
            description="Identifier of the email campaign group.",
        ),
        th.Property(
            "emailTemplateMode",
            th.StringType,
            description="Template mode for the email (e.g. DRAG_AND_DROP).",
        ),
        th.Property(
            "from",
            th.ObjectType(
                th.Property(
                    "customReplyTo",
                    th.StringType,
                    description="Custom reply-to address.",
                ),
                th.Property(
                    "fromName",
                    th.StringType,
                    description="Display name of the sender.",
                ),
                th.Property(
                    "replyTo",
                    th.StringType,
                    description="Reply-to email address.",
                ),
            ),
            description="Sender information for the email.",
        ),
        th.Property(
            "isAb",
            th.BooleanType,
            description="Whether this is an A/B test email.",
        ),
        th.Property(
            "isPublished",
            th.BooleanType,
            description="Whether the email has been published.",
        ),
        th.Property(
            "isTransactional",
            th.BooleanType,
            description="Whether this is a transactional email.",
        ),
        th.Property(
            "jitterSendTime",
            th.BooleanType,
            description="Whether send time jitter is enabled.",
        ),
        th.Property(
            "language",
            th.StringType,
            description="Language of the email content.",
        ),
        th.Property(
            "name",
            th.StringType,
            description="Name of the record.",
        ),
        th.Property(
            "previewKey",
            th.StringType,
            description="Key used for email preview.",
        ),
        th.Property(
            "primaryEmailCampaignId",
            th.StringType,
            description="Identifier of the primary email campaign.",
        ),
        th.Property(
            "publishDate",
            th.StringType,
            description="Scheduled or actual publish date.",
        ),
        th.Property(
            "publishedAt",
            th.StringType,
            description="Timestamp when the email was published.",
        ),
        th.Property(
            "publishedByEmail",
            th.StringType,
            description="Email of the user who published.",
        ),
        th.Property(
            "publishedById",
            th.StringType,
            description="Identifier of the user who published.",
        ),
        th.Property(
            "publishedByName",
            th.StringType,
            description="Name of the user who published.",
        ),
        th.Property(
            "sendOnPublish",
            th.BooleanType,
            description="Whether to send immediately on publish.",
        ),
        th.Property(
            "state",
            th.StringType,
            description="Current status of the record.",
        ),
        th.Property(
            "stats",
            th.ObjectType(
                th.Property(
                    "counters",
                    th.ObjectType(
                        th.Property(
                            "bounce",
                            th.IntegerType,
                            description="Number of bounce events.",
                        ),
                        th.Property(
                            "click",
                            th.IntegerType,
                            description="Number of click events.",
                        ),
                        th.Property(
                            "contactslost",
                            th.IntegerType,
                            description="Number of contacts lost.",
                        ),
                        th.Property(
                            "delivered",
                            th.IntegerType,
                            description="Number of emails delivered.",
                        ),
                        th.Property(
                            "dropped",
                            th.IntegerType,
                            description="Number of emails dropped.",
                        ),
                        th.Property(
                            "hardbounced",
                            th.IntegerType,
                            description="Number of hard bounces.",
                        ),
                        th.Property(
                            "notsent",
                            th.IntegerType,
                            description="Number of emails not sent.",
                        ),
                        th.Property(
                            "open",
                            th.IntegerType,
                            description="Number of open events.",
                        ),
                        th.Property(
                            "pending",
                            th.IntegerType,
                            description="Number of pending sends.",
                        ),
                        th.Property(
                            "reply",
                            th.IntegerType,
                            description="Number of reply events.",
                        ),
                        th.Property(
                            "selected",
                            th.IntegerType,
                            description="Number of selected recipients.",
                        ),
                        th.Property(
                            "sent",
                            th.IntegerType,
                            description="Number of emails sent.",
                        ),
                        th.Property(
                            "softbounced",
                            th.IntegerType,
                            description="Number of soft bounces.",
                        ),
                        th.Property(
                            "spamreport",
                            th.IntegerType,
                            description="Number of spam reports.",
                        ),
                        th.Property(
                            "suppressed",
                            th.IntegerType,
                            description="Number of suppressed sends.",
                        ),
                        th.Property(
                            "unsubscribed",
                            th.IntegerType,
                            description="Number of unsubscribe events.",
                        ),
                    ),
                    description="Email performance counters.",
                ),
                th.Property(
                    "deviceBreakdown",
                    th.ObjectType(
                        th.Property(
                            "click_device_type",
                            th.ObjectType(
                                th.Property(
                                    "computer",
                                    th.IntegerType,
                                    description="Clicks from computer devices.",
                                ),
                                th.Property(
                                    "mobile",
                                    th.IntegerType,
                                    description="Clicks from mobile devices.",
                                ),
                                th.Property(
                                    "unknown",
                                    th.IntegerType,
                                    description="Clicks from unknown devices.",
                                ),
                            ),
                            description="Click counts by device type.",
                        ),
                        th.Property(
                            "open_device_type",
                            th.ObjectType(
                                th.Property(
                                    "computer",
                                    th.IntegerType,
                                    description="Opens from computer devices.",
                                ),
                                th.Property(
                                    "mobile",
                                    th.IntegerType,
                                    description="Opens from mobile devices.",
                                ),
                                th.Property(
                                    "unknown",
                                    th.IntegerType,
                                    description="Opens from unknown devices.",
                                ),
                            ),
                            description="Open counts by device type.",
                        ),
                    ),
                    description="Email engagement breakdown by device.",
                ),
                th.Property(
                    "qualifierStats",
                    th.ObjectType(),
                    description="Qualifier statistics for the email.",
                ),
                th.Property(
                    "ratios",
                    th.ObjectType(
                        th.Property(
                            "bounceratio",
                            th.IntegerType,
                            description="Bounce ratio.",
                        ),
                        th.Property(
                            "clickratio",
                            th.IntegerType,
                            description="Click ratio.",
                        ),
                        th.Property(
                            "clickthroughratio",
                            th.IntegerType,
                            description="Click-through ratio.",
                        ),
                        th.Property(
                            "contactslostratio",
                            th.IntegerType,
                            description="Contacts lost ratio.",
                        ),
                        th.Property(
                            "deliveredratio",
                            th.IntegerType,
                            description="Delivered ratio.",
                        ),
                        th.Property(
                            "hardbounceratio",
                            th.IntegerType,
                            description="Hard bounce ratio.",
                        ),
                        th.Property(
                            "notsentratio",
                            th.IntegerType,
                            description="Not sent ratio.",
                        ),
                        th.Property(
                            "openratio",
                            th.IntegerType,
                            description="Open ratio.",
                        ),
                        th.Property(
                            "pendingratio",
                            th.IntegerType,
                            description="Pending ratio.",
                        ),
                        th.Property(
                            "replyratio",
                            th.IntegerType,
                            description="Reply ratio.",
                        ),
                        th.Property(
                            "softbounceratio",
                            th.IntegerType,
                            description="Soft bounce ratio.",
                        ),
                        th.Property(
                            "spamreportratio",
                            th.IntegerType,
                            description="Spam report ratio.",
                        ),
                        th.Property(
                            "unsubscribedratio",
                            th.IntegerType,
                            description="Unsubscribe ratio.",
                        ),
                    ),
                    description="Email performance ratios.",
                ),
            ),
            description="Email performance statistics.",
        ),
        th.Property(
            "subcategory",
            th.StringType,
            description="Subcategory classification of the email.",
        ),
        th.Property(
            "subject",
            th.StringType,
            description="Subject line of the email.",
        ),
        th.Property(
            "subscriptionDetails",
            th.ObjectType(
                th.Property(
                    "officeLocationId",
                    th.StringType,
                    description="Identifier of the office location.",
                ),
                th.Property(
                    "subscriptionId",
                    th.StringType,
                    description="Identifier of the subscription.",
                ),
                th.Property(
                    "subscriptionName",
                    th.StringType,
                    description="Name of the subscription.",
                ),
            ),
            description="Subscription details for the email.",
        ),
        th.Property(
            "to",
            th.ObjectType(
                th.Property(
                    "contactIds",
                    th.ObjectType(
                        th.Property(
                            "exclude",
                            th.ArrayType(th.StringType),
                            description="Contact IDs to exclude from the send.",
                        ),
                        th.Property(
                            "include",
                            th.ArrayType(th.StringType),
                            description="Contact IDs to include in the send.",
                        ),
                    ),
                    description="Contact ID targeting.",
                ),
                th.Property(
                    "contactIlsLists",
                    th.ObjectType(
                        th.Property(
                            "exclude",
                            th.ArrayType(th.StringType),
                            description="Lists to exclude.",
                        ),
                        th.Property(
                            "include",
                            th.ArrayType(th.StringType),
                            description="Lists to include.",
                        ),
                    ),
                    description="Contact list targeting.",
                ),
                th.Property(
                    "contactLists",
                    th.ObjectType(
                        th.Property(
                            "exclude",
                            th.ArrayType(th.StringType),
                            description="Contact list IDs to exclude.",
                        ),
                        th.Property(
                            "include",
                            th.ArrayType(th.StringType),
                            description="Contact list IDs to include.",
                        ),
                    ),
                    description="Contact list targeting.",
                ),
                th.Property(
                    "suppressGraymail",
                    th.BooleanType,
                    description="Whether to suppress graymail.",
                ),
            ),
            description="Recipient targeting configuration.",
        ),
        th.Property(
            "type",
            th.StringType,
            description="Type classification of the record.",
        ),
        th.Property(
            "updatedAt",
            th.StringType,
            description="Timestamp when the record was last updated.",
        ),
        th.Property(
            "updatedById",
            th.StringType,
            description="Identifier of the user who last updated the email.",
        ),
        th.Property(
            "webversion",
            th.ObjectType(
                th.Property(
                    "domain",
                    th.StringType,
                    description="Domain for the web version.",
                ),
                th.Property(
                    "enabled",
                    th.BooleanType,
                    description="Whether web version is enabled.",
                ),
                th.Property(
                    "isPageRedirected",
                    th.BooleanType,
                    description="Whether the page uses redirect.",
                ),
                th.Property(
                    "slug",
                    th.StringType,
                    description="URL slug for the web version.",
                ),
                th.Property(
                    "url",
                    th.StringType,
                    description="URL of the web version.",
                ),
            ),
            description="Web version settings for the email.",
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
