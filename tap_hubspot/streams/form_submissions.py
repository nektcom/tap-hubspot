from __future__ import annotations

from nekt_singer_sdk import typing as th  # JSON Schema typing helpers
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
    parent_stream = FormsStream
    state_partitioning_keys = ["form_id"]

    schema = th.PropertiesList(
        th.Property("conversionId", th.StringType),
        th.Property("submittedAt", th.IntegerType),
        th.Property(
            "values",
            th.ArrayType(
                th.ObjectType(
                    th.Property("name", th.StringType),
                    th.Property("value", th.StringType),
                )
            ),
        ),
        th.Property("pageUrl", th.StringType),
    ).to_dict()

    @property
    def url_base(self) -> str:
        """
        Returns an updated path which includes the api version
        """
        return "https://api.hubapi.com/form-integrations/v1"
