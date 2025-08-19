from __future__ import annotations

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
from tap_hubspot.client import HubspotStream


class FormsStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/marketing/forms
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "forms"
    path = "/forms"
    primary_keys = ["id"]
    records_jsonpath = "$[results][*]"
    page_size = 50

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("updatedAt", th.DateTimeType),
        th.Property("archived", th.BooleanType),
        th.Property("formType", th.StringType),
        th.Property(
            "fieldGroups",
            th.ArrayType(
                th.ObjectType(
                    th.Property("groupType", th.StringType),
                    th.Property("richTextType", th.StringType),
                    th.Property(
                        "fields",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("objectTypeId", th.StringType),
                                th.Property("name", th.StringType),
                                th.Property("label", th.StringType),
                                th.Property("required", th.BooleanType),
                                th.Property("hidden", th.BooleanType),
                                th.Property("fieldType", th.StringType),
                                th.Property(
                                    "validation",
                                    th.ObjectType(
                                        th.Property("blockedEmailDomains", th.ArrayType(th.StringType)),
                                        th.Property("useDefaultBlockList", th.BooleanType),
                                    ),
                                ),
                            )
                        ),
                    ),
                )
            ),
        ),
        th.Property(
            "configuration",
            th.ObjectType(
                th.Property("language", th.StringType),
                th.Property("cloneable", th.BooleanType),
                th.Property(
                    "postSubmitAction",
                    th.ObjectType(
                        th.Property("type", th.StringType),
                        th.Property("value", th.StringType),
                    ),
                ),
                th.Property("editable", th.BooleanType),
                th.Property("archivable", th.BooleanType),
                th.Property("recaptchaEnabled", th.BooleanType),
                th.Property("notifyContactOwner", th.BooleanType),
                th.Property("notifyRecipients", th.ArrayType(th.StringType)),
                th.Property("createNewContactForNewEmail", th.BooleanType),
                th.Property("prePopulateKnownValues", th.BooleanType),
                th.Property("allowLinkToResetKnownValues", th.BooleanType),
                th.Property(
                    "lifecycleStages",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property("objectTypeId", th.StringType),
                            th.Property("value", th.StringType),
                        )
                    ),
                ),
            ),
        ),
        th.Property(
            "displayOptions",
            th.ObjectType(
                th.Property("renderRawHtml", th.BooleanType),
                th.Property("theme", th.StringType),
                th.Property("submitButtonText", th.StringType),
                th.Property(
                    "style",
                    th.ObjectType(
                        th.Property("fontFamily", th.StringType),
                        th.Property("backgroundWidth", th.StringType),
                        th.Property("labelTextColor", th.StringType),
                        th.Property("labelTextSize", th.StringType),
                        th.Property("helpTextColor", th.StringType),
                        th.Property("helpTextSize", th.StringType),
                        th.Property("legalConsentTextColor", th.StringType),
                        th.Property("legalConsentTextSize", th.StringType),
                        th.Property("submitColor", th.StringType),
                        th.Property("submitAlignment", th.StringType),
                        th.Property("submitFontColor", th.StringType),
                        th.Property("submitSize", th.StringType),
                    ),
                ),
                th.Property("cssClass", th.StringType),
            ),
        ),
        th.Property(
            "legalConsentOptions",
            th.ObjectType(
                th.Property("type", th.StringType),
            ),
        ),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/marketing/v3"

    def get_child_context(self, record: dict) -> dict:
        """
        Returns a child context for the form submissions stream
        """
        return {"form_id": record["id"]}
