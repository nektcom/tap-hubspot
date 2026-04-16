from __future__ import annotations

from functools import cached_property

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
from tap_hubspot.client import DynamicIncrementalHubspotStream, sanitize_association_key


class LeadsStream(DynamicIncrementalHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/leads
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "leads"
    path = "/objects/leads"
    incremental_path = "/objects/leads/search"
    primary_keys = ["id"]
    replication_key = "hs_lastmodifieddate"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @cached_property
    def associations_string_list(self) -> list[str]:
        return self.config.get("extract_lead_associations_comma_separated_string").replace(" ", "").split(",")

    @cached_property
    def property_history_string_list(self) -> list[str]:
        return self.config.get("extract_lead_property_history_comma_separated_string").replace(" ", "").split(",")

    @cached_property
    def should_extract_associations(self) -> bool:
        return self.config.get("extract_lead_associations") and self.associations_string_list

    @cached_property
    def should_extract_property_history(self) -> bool:
        return self.config.get("extract_lead_property_history") and self.property_history_string_list

    @cached_property
    def schema(self) -> dict:
        schema = super().schema
        if self.should_extract_associations:
            associations_schema = th.PropertiesList()
            for association_string in self.associations_string_list:
                associations_schema.append(
                    th.Property(
                        sanitize_association_key(association_string),
                        th.ArrayType(
                            th.ObjectType(
                                th.Property(
                                    "id",
                                    th.StringType,
                                    description="Unique identifier of the associated record.",
                                ),
                                th.Property(
                                    "type",
                                    th.StringType,
                                    description="Type classification of the association.",
                                ),
                            )
                        ),
                        description="List of associated records.",
                    )
                )

            schema["properties"]["associations"] = associations_schema.to_dict()
        if self.should_extract_property_history:
            property_history_schema = th.PropertiesList()
            property_history_properties = th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "sourceType",
                        th.StringType,
                        description="Type of the change source.",
                    ),
                    th.Property(
                        "sourceId",
                        th.StringType,
                        description="Identifier of the change source.",
                    ),
                    th.Property(
                        "updatedByUserId",
                        th.IntegerType,
                        description="Identifier of the user who made the change.",
                    ),
                    th.Property(
                        "value",
                        th.StringType,
                        description="Value of the property at this change.",
                    ),
                    th.Property(
                        "timestamp",
                        th.StringType,
                        description="Timestamp when the change occurred.",
                    ),
                )
            )
            for property_name in self.property_history_string_list:
                property_history_schema.append(
                    th.Property(
                        property_name,
                        property_history_properties,
                        description="History of changes for this property.",
                    )
                )
            schema["properties"]["propertiesWithHistory"] = property_history_schema.to_dict()
        return schema

    def post_process(self, row, context=None):
        if not (self.should_extract_associations or self.should_extract_property_history):
            return super().post_process(row, context)

        additional_data = self._fetch_additional_data_with_retry(
            "leads",
            row["id"],
            self.associations_string_list if self.should_extract_associations else None,
            self.property_history_string_list if self.should_extract_property_history else None,
        )

        if "associations" in additional_data:
            row["associations"] = additional_data["associations"]
        if "propertiesWithHistory" in additional_data:
            row["propertiesWithHistory"] = additional_data["propertiesWithHistory"]

        return super().post_process(row, context)

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"
