from __future__ import annotations

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
from nekt_singer_sdk.helpers.types import Context, Record
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
        th.Property(
            "id",
            th.StringType,
            description="Unique identifier of the record.",
        ),
        th.Property(
            "name",
            th.StringType,
            description="Name of the record.",
        ),
        th.Property(
            "createdAt",
            th.DateTimeType,
            description="Timestamp when the record was created.",
        ),
        th.Property(
            "updatedAt",
            th.DateTimeType,
            description="Timestamp when the record was last updated.",
        ),
        th.Property(
            "archived",
            th.BooleanType,
            description="Whether the record is archived.",
        ),
        th.Property(
            "formType",
            th.StringType,
            description="Type classification of the form.",
        ),
        th.Property(
            "fieldGroups",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "groupType",
                        th.StringType,
                        description="Type of the field group.",
                    ),
                    th.Property(
                        "richTextType",
                        th.StringType,
                        description="Rich text type for the group.",
                    ),
                    th.Property(
                        "fields",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property(
                                    "objectTypeId",
                                    th.StringType,
                                    description="Identifier of the object type.",
                                ),
                                th.Property(
                                    "name",
                                    th.StringType,
                                    description="Name of the form field.",
                                ),
                                th.Property(
                                    "label",
                                    th.StringType,
                                    description="Display label for the field.",
                                ),
                                th.Property(
                                    "required",
                                    th.BooleanType,
                                    description="Whether the field is required.",
                                ),
                                th.Property(
                                    "hidden",
                                    th.BooleanType,
                                    description="Whether the field is hidden.",
                                ),
                                th.Property(
                                    "fieldType",
                                    th.StringType,
                                    description="Type of the form field.",
                                ),
                                th.Property(
                                    "useCountryCodeSelect",
                                    th.BooleanType,
                                    description="Whether to use country code select.",
                                ),
                                th.Property(
                                    "options",
                                    th.ArrayType(
                                        th.ObjectType(
                                            th.Property(
                                                "label",
                                                th.StringType,
                                                description="Display label for the option.",
                                            ),
                                            th.Property(
                                                "value",
                                                th.StringType,
                                                description="Value of the option.",
                                            ),
                                            th.Property(
                                                "description",
                                                th.StringType,
                                                description="Description of the option.",
                                            ),
                                            th.Property(
                                                "displayOrder",
                                                th.IntegerType,
                                                description="Order in which the option is displayed.",
                                            ),
                                        )
                                    ),
                                    description="List of options for the field.",
                                ),
                                th.Property(
                                    "validation",
                                    th.ObjectType(
                                        th.Property(
                                            "blockedEmailDomains",
                                            th.ArrayType(th.StringType),
                                            description="List of blocked email domains.",
                                        ),
                                        th.Property(
                                            "useDefaultBlockList",
                                            th.BooleanType,
                                            description="Whether to use the default block list.",
                                        ),
                                        th.Property(
                                            "minAllowedDigits",
                                            th.IntegerType,
                                            description="Minimum allowed digits.",
                                        ),
                                        th.Property(
                                            "maxAllowedDigits",
                                            th.IntegerType,
                                            description="Maximum allowed digits.",
                                        ),
                                        th.Property(
                                            "minAllowedCharacters",
                                            th.IntegerType,
                                            description="Minimum allowed characters.",
                                        ),
                                        th.Property(
                                            "maxAllowedCharacters",
                                            th.IntegerType,
                                            description="Maximum allowed characters.",
                                        ),
                                    ),
                                    description="Validation rules for the field.",
                                ),
                            )
                        ),
                        description="List of form fields in the group.",
                    ),
                )
            ),
            description="List of field groups in the form.",
        ),
        th.Property(
            "configuration",
            th.ObjectType(
                th.Property(
                    "language",
                    th.StringType,
                    description="Language of the form.",
                ),
                th.Property(
                    "cloneable",
                    th.BooleanType,
                    description="Whether the form can be cloned.",
                ),
                th.Property(
                    "postSubmitAction",
                    th.ObjectType(
                        th.Property(
                            "type",
                            th.StringType,
                            description="Type of post-submit action.",
                        ),
                        th.Property(
                            "value",
                            th.StringType,
                            description="Value for the post-submit action.",
                        ),
                    ),
                    description="Action to perform after form submission.",
                ),
                th.Property(
                    "editable",
                    th.BooleanType,
                    description="Whether the form is editable.",
                ),
                th.Property(
                    "archivable",
                    th.BooleanType,
                    description="Whether the form can be archived.",
                ),
                th.Property(
                    "recaptchaEnabled",
                    th.BooleanType,
                    description="Whether reCAPTCHA is enabled.",
                ),
                th.Property(
                    "notifyContactOwner",
                    th.BooleanType,
                    description="Whether to notify the contact owner on submission.",
                ),
                th.Property(
                    "notifyRecipients",
                    th.ArrayType(th.StringType),
                    description="List of recipients to notify on submission.",
                ),
                th.Property(
                    "createNewContactForNewEmail",
                    th.BooleanType,
                    description="Whether to create a new contact for new email submissions.",
                ),
                th.Property(
                    "prePopulateKnownValues",
                    th.BooleanType,
                    description="Whether to pre-populate known contact values.",
                ),
                th.Property(
                    "allowLinkToResetKnownValues",
                    th.BooleanType,
                    description="Whether to allow link to reset known values.",
                ),
                th.Property(
                    "lifecycleStages",
                    th.ArrayType(
                        th.ObjectType(
                            th.Property(
                                "objectTypeId",
                                th.StringType,
                                description="Identifier of the object type.",
                            ),
                            th.Property(
                                "value",
                                th.StringType,
                                description="Lifecycle stage value.",
                            ),
                        )
                    ),
                    description="Lifecycle stages for the form.",
                ),
            ),
            description="Form configuration settings.",
        ),
        th.Property(
            "displayOptions",
            th.ObjectType(
                th.Property(
                    "renderRawHtml",
                    th.BooleanType,
                    description="Whether to render raw HTML.",
                ),
                th.Property(
                    "theme",
                    th.StringType,
                    description="Display theme for the form.",
                ),
                th.Property(
                    "submitButtonText",
                    th.StringType,
                    description="Text displayed on the submit button.",
                ),
                th.Property(
                    "style",
                    th.ObjectType(
                        th.Property(
                            "fontFamily",
                            th.StringType,
                            description="Font family for the form.",
                        ),
                        th.Property(
                            "backgroundWidth",
                            th.StringType,
                            description="Background width setting.",
                        ),
                        th.Property(
                            "labelTextColor",
                            th.StringType,
                            description="Color of the label text.",
                        ),
                        th.Property(
                            "labelTextSize",
                            th.StringType,
                            description="Size of the label text.",
                        ),
                        th.Property(
                            "helpTextColor",
                            th.StringType,
                            description="Color of the help text.",
                        ),
                        th.Property(
                            "helpTextSize",
                            th.StringType,
                            description="Size of the help text.",
                        ),
                        th.Property(
                            "legalConsentTextColor",
                            th.StringType,
                            description="Color of the legal consent text.",
                        ),
                        th.Property(
                            "legalConsentTextSize",
                            th.StringType,
                            description="Size of the legal consent text.",
                        ),
                        th.Property(
                            "submitColor",
                            th.StringType,
                            description="Color of the submit button.",
                        ),
                        th.Property(
                            "submitAlignment",
                            th.StringType,
                            description="Alignment of the submit button.",
                        ),
                        th.Property(
                            "submitFontColor",
                            th.StringType,
                            description="Font color of the submit button.",
                        ),
                        th.Property(
                            "submitSize",
                            th.StringType,
                            description="Size of the submit button.",
                        ),
                    ),
                    description="Style settings for the form display.",
                ),
                th.Property(
                    "cssClass",
                    th.StringType,
                    description="CSS class for the form.",
                ),
            ),
            description="Display options for the form.",
        ),
        th.Property(
            "legalConsentOptions",
            th.ObjectType(
                th.Property(
                    "type",
                    th.StringType,
                    description="Type of legal consent.",
                ),
            ),
            description="Legal consent options for the form.",
        ),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/marketing/v3"

    def get_child_context(
        self,
        record: Record,
        context: Context | None,
    ) -> Context | None:
        """
        Returns a child context for the form submissions stream
        """
        return {"form_id": record["id"]}
