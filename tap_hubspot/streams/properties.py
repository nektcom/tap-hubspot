"""Properties stream for tap-hubspot."""

from __future__ import annotations

from nekt_singer_sdk import typing as th
from tap_hubspot.client import HubspotStream
from typing_extensions import override

PropertiesList = th.PropertiesList
Property = th.Property
ObjectType = th.ObjectType
DateTimeType = th.DateTimeType
StringType = th.StringType
ArrayType = th.ArrayType
BooleanType = th.BooleanType
IntegerType = th.IntegerType


class PropertiesStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/properties

    Fetches CRM property definitions for one or more HubSpot object types in a
    single stream. The object types to fetch are controlled by the
    ``property_objects`` config key (defaults to all standard object types).
    Each record includes a ``hubspot_object`` field identifying its source type.
    """

    name = "properties"
    path = "/properties/{object_type}"
    primary_keys = ["name", "hubspot_object"]
    records_jsonpath = "$[results][*]"
    schema = PropertiesList(
        Property(
            "updatedAt",
            StringType,
            description="Timestamp when the record was last updated.",
        ),
        Property(
            "createdAt",
            StringType,
            description="Timestamp when the record was created.",
        ),
        Property(
            "name",
            StringType,
            description="Internal name of the property.",
        ),
        Property(
            "label",
            StringType,
            description="Display label of the property.",
        ),
        Property(
            "type",
            StringType,
            description="Type classification of the record.",
        ),
        Property(
            "fieldType",
            StringType,
            description="Field type used in forms and UI.",
        ),
        Property(
            "description",
            StringType,
            description="Description of the property.",
        ),
        Property(
            "groupName",
            StringType,
            description="Name of the property group.",
        ),
        Property(
            "options",
            ArrayType(
                ObjectType(
                    Property(
                        "label",
                        StringType,
                        description="Display label for the option.",
                    ),
                    Property(
                        "description",
                        StringType,
                        description="Description of the option.",
                    ),
                    Property(
                        "value",
                        StringType,
                        description="Value of the option.",
                    ),
                    Property(
                        "displayOrder",
                        IntegerType,
                        description="Order in which the option is displayed.",
                    ),
                    Property(
                        "hidden",
                        BooleanType,
                        description="Whether the option is hidden.",
                    ),
                ),
            ),
            description="List of options for the property.",
        ),
        Property(
            "displayOrder",
            IntegerType,
            description="Order in which the property is displayed.",
        ),
        Property(
            "calculated",
            BooleanType,
            description="Whether the property is calculated.",
        ),
        Property(
            "externalOptions",
            BooleanType,
            description="Whether the property uses external options.",
        ),
        Property(
            "hasUniqueValue",
            BooleanType,
            description="Whether the property must have a unique value.",
        ),
        Property(
            "hidden",
            BooleanType,
            description="Whether the property is hidden.",
        ),
        Property(
            "hubspotDefined",
            BooleanType,
            description="Whether the property is defined by HubSpot.",
        ),
        Property(
            "modificationMetadata",
            ObjectType(
                Property(
                    "readOnlyOptions",
                    BooleanType,
                    description="Whether options are read-only.",
                ),
                Property(
                    "readOnlyValue",
                    BooleanType,
                    description="Whether the value is read-only.",
                ),
                Property(
                    "readOnlyDefinition",
                    BooleanType,
                    description="Whether the definition is read-only.",
                ),
                Property(
                    "archivable",
                    BooleanType,
                    description="Whether the property can be archived.",
                ),
            ),
            description="Metadata about property modification permissions.",
        ),
        Property(
            "formField",
            BooleanType,
            description="Whether the property is used in forms.",
        ),
        Property(
            "hubspot_object",
            StringType,
            description="HubSpot object type the property belongs to.",
        ),
        Property(
            "createdUserId",
            StringType,
            description="ID of the user who created the property.",
        ),
        Property(
            "updatedUserId",
            StringType,
            description="ID of the user who last updated the property.",
        ),
        Property(
            "referencedObjectType",
            StringType,
            description="Object type referenced by this property (e.g. OWNER).",
        ),
        Property(
            "calculationFormula",
            StringType,
            description="Formula used for calculated properties.",
        ),
        Property(
            "archived",
            BooleanType,
            description="Whether the property is archived.",
        ),
        Property(
            "dataSensitivity",
            StringType,
            description="Data sensitivity level of the property.",
        ),
    ).to_dict()

    @property
    def url_base(self) -> str:
        return "https://api.hubapi.com/crm/v3"

    @property
    def partitions(self) -> list[dict]:
        raw = self.config.get("property_objects")
        objects = [obj.strip() for obj in raw.split(",")]
        return [{"object_type": obj} for obj in objects]

    @override
    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        row["hubspot_object"] = (context or {}).get("object_type")
        return row
