from __future__ import annotations

from functools import cached_property

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
from tap_hubspot.client import DynamicIncrementalHubspotStream, sanitize_association_key


class CompanyStream(DynamicIncrementalHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/companies
    """

    """
    name: stream name
    path: path which will be added to api url in client.py
    schema: instream schema
    primary_keys = primary keys for the table
    replication_key = datetime keys for replication
    records_jsonpath = json response body
    """

    name = "companies"
    path = "/objects/companies"
    incremental_path = "/objects/companies/search"
    primary_keys = ["id"]
    replication_key = "hs_lastmodifieddate"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @cached_property
    def associations_string_list(self) -> list[str]:
        return self.config.get("extract_company_associations_comma_separated_string").replace(" ", "").split(",")

    @cached_property
    def should_extract_associations(self) -> bool:
        return self.config.get("extract_company_associations") and self.associations_string_list

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
        return schema

    def post_process(self, row, context=None):
        if not self.should_extract_associations:
            return super().post_process(row, context)

        additional_data = self._fetch_additional_data_with_retry(
            "companies",
            row["id"],
            self.associations_string_list,
        )

        if "associations" in additional_data:
            row["associations"] = additional_data["associations"]

        return super().post_process(row, context)

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"
