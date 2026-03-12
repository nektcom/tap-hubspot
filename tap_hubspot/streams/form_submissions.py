from __future__ import annotations

from typing import Any, Mapping

from nekt_singer_sdk import typing as th
from tap_hubspot.client import HubspotStream
from tap_hubspot.streams.forms import FormsStream


class FormSubmissionsStream(HubspotStream):
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

    name = "form_submissions"
    path = "/submissions/forms/{form_id}"
    primary_keys = ["conversionId"]
    records_jsonpath = "$[results][*]"
    replication_key = "submittedAt"
    parent_stream_type = FormsStream
    state_partitioning_keys = ["form_id"]
    page_size = 50

    schema = th.PropertiesList(
        th.Property(
            "conversionId",
            th.StringType,
            description="Unique identifier of the form submission.",
        ),
        th.Property(
            "formId",
            th.StringType,
            description="Identifier of the associated form.",
        ),
        th.Property(
            "submittedAt",
            th.IntegerType,
            description="Timestamp when the form was submitted.",
        ),
        th.Property(
            "values",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "objectTypeId",
                        th.StringType,
                        description="Identifier of the object type for the field.",
                    ),
                    th.Property(
                        "name",
                        th.StringType,
                        description="Name of the form field.",
                    ),
                    th.Property(
                        "value",
                        th.StringType,
                        description="Value submitted for the field.",
                    ),
                )
            ),
            description="List of submitted form field values.",
        ),
        th.Property(
            "pageUrl",
            th.StringType,
            description="URL of the page where the form was submitted.",
        ),
    ).to_dict()

    def post_process(self, row: dict[str, Any], context: Mapping[str, Any] | None = None) -> dict | None:
        row["formId"] = context["form_id"]
        return super().post_process(row, context)

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/form-integrations/v1"
