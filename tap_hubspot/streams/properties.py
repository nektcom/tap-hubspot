"""Stream type classes for tap-hubspot."""

from __future__ import annotations

from typing import Any, Iterable

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
from tap_hubspot.client import HubspotStream

PropertiesList = th.PropertiesList
Property = th.Property
ObjectType = th.ObjectType
DateTimeType = th.DateTimeType
StringType = th.StringType
ArrayType = th.ArrayType
BooleanType = th.BooleanType
IntegerType = th.IntegerType


class PropertyTicketStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_tickets"
    path = "/properties/tickets"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

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
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyDealStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_deals"
    path = "/properties/deals"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

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
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyContactStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_contacts"
    path = "/properties/contacts"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

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
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyCompanyStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_companies"
    path = "/properties/company"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

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
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyProductStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_products"
    path = "/properties/product"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

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
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyLineItemStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_line_items"
    path = "/properties/line_item"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

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
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyEmailStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_emails"
    path = "/properties/email"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

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
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyPostalMailStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_postal_mails"
    path = "/properties/postal_mail"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

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
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyCallStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_calls"
    path = "/properties/call"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

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
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyMeetingStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_meetings"
    path = "/properties/meeting"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

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
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyTaskStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_tasks"
    path = "/properties/task"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

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
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyCommunicationStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "property_communications"
    path = "/properties/communication"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

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
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"


class PropertyNotesStream(HubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/properties#endpoint?spec=PATCH-/crm/v3/properties/{objectType}/{propertyName}
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "properties"
    path = "/properties/notes"
    primary_keys = ["label"]
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

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
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"

    def get_records(self, context: dict | None) -> Iterable[dict[str, Any]]:
        """
        Merges all the property stream data into a single property table
        """

        property_ticket = PropertyTicketStream(self._tap, schema={"properties": {}})
        property_deal = PropertyDealStream(self._tap, schema={"properties": {}})
        property_contact = PropertyContactStream(self._tap, schema={"properties": {}})
        property_company = PropertyCompanyStream(self._tap, schema={"properties": {}})
        property_product = PropertyProductStream(self._tap, schema={"properties": {}})
        property_lineitem = PropertyLineItemStream(self._tap, schema={"properties": {}})
        property_email = PropertyEmailStream(self._tap, schema={"properties": {}})
        property_postalmail = PropertyPostalMailStream(self._tap, schema={"properties": {}})
        property_call = PropertyCallStream(self._tap, schema={"properties": {}})
        property_meeting = PropertyMeetingStream(self._tap, schema={"properties": {}})
        property_task = PropertyTaskStream(self._tap, schema={"properties": {}})
        property_communication = PropertyCommunicationStream(self._tap, schema={"properties": {}})
        property_records = (
            list(property_ticket.get_records(context))
            + list(property_deal.get_records(context))
            + list(property_contact.get_records(context))
            + list(property_company.get_records(context))
            + list(property_product.get_records(context))
            + list(property_lineitem.get_records(context))
            + list(property_email.get_records(context))
            + list(property_postalmail.get_records(context))
            + list(property_call.get_records(context))
            + list(property_meeting.get_records(context))
            + list(property_task.get_records(context))
            + list(property_communication.get_records(context))
            + list(super().get_records(context))
        )

        return property_records
