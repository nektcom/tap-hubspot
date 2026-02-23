from __future__ import annotations

from functools import cached_property

import requests
from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
from tap_hubspot.client import DynamicIncrementalHubspotStream


class EmailStream(DynamicIncrementalHubspotStream):
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

    name = "emails"
    path = "/objects/emails"
    primary_keys = ["id"]
    incremental_path = "/objects/emails/search"
    replication_key = "hs_lastmodifieddate"
    records_jsonpath = "$[results][*]"  # Or override `parse_response`.

    @cached_property
    def associations_string_list(self) -> list[str]:
        return self.config.get("extract_email_associations_comma_separated_string").replace(" ", "").split(",")

    @cached_property
    def should_extract_associations(self) -> bool:
        return self.config.get("extract_email_associations") and self.associations_string_list

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
        return schema

    def post_process(self, row, context=None):
        if not self.should_extract_associations:
            return super().post_process(row, context)

        additional_data = self._fetch_additional_data_with_retry(
            "emails",
            row["id"],
            self.associations_string_list,
        )

        if "associations" in additional_data:
            row["associations"] = additional_data["associations"]

        return super().post_process(row, context)

    def validate_response(self, response: requests.Response) -> None:
        return super().validate_response(response)

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/crm/v3"
