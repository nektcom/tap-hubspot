from __future__ import annotations

from functools import cached_property

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
from tap_hubspot.client import DynamicIncrementalHubspotStream


class ContactStream(DynamicIncrementalHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/contacts
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "contacts"
    path = "/objects/contacts"
    incremental_path = "/objects/contacts/search"
    primary_keys = ["id"]
    replication_key = "lastmodifieddate"
    replication_method = "INCREMENTAL"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @cached_property
    def associations_string_list(self) -> list[str]:
        return self.config.get("extract_contact_associations_comma_separated_string").replace(" ", "").split(",")

    @cached_property
    def property_history_string_list(self) -> list[str]:
        return self.config.get("extract_contact_property_history_comma_separated_string").replace(" ", "").split(",")

    @cached_property
    def should_extract_associations(self) -> bool:
        return self.config.get("extract_contact_associations") and self.associations_string_list

    @cached_property
    def should_extract_property_history(self) -> bool:
        return self.config.get("extract_contact_property_history") and self.property_history_string_list

    @cached_property
    def schema(self) -> dict:
        schema = super().schema
        if self.should_extract_associations:
            associations_schema = th.PropertiesList()
            for association_string in self.associations_string_list:
                associations_schema.append(
                    th.Property(
                        association_string,
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("id", th.StringType),
                                th.Property("type", th.StringType),
                            )
                        ),
                    )
                )

            schema["properties"]["associations"] = associations_schema.to_dict()
        if self.should_extract_property_history:
            property_history_schema = th.PropertiesList()
            property_history_properties = th.ArrayType(
                th.ObjectType(
                    th.Property("sourceType", th.StringType),
                    th.Property("sourceId", th.StringType),
                    th.Property("updatedByUserId", th.StringType),
                    th.Property("value", th.StringType),
                    th.Property("timestamp", th.StringType),
                )
            )
            for property_name in self.property_history_string_list:
                property_history_schema.append(th.Property(property_name, property_history_properties))
            schema["properties"]["propertiesWithHistory"] = property_history_schema.to_dict()
        return schema

    def post_process(self, row, context=None):
        if not (self.should_extract_associations or self.should_extract_property_history):
            return super().post_process(row, context)

        additional_data = self._fetch_additional_data_with_retry(
            "contacts",
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
