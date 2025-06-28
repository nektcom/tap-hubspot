"""tap-hubspot tap class."""

from __future__ import annotations

import sys

import requests
from nekt_singer_sdk import typing as th
from nekt_singer_sdk.custom_logger import user_logger
from nekt_singer_sdk.tap_base import Tap
from tap_hubspot import streams


class TapHubspot(Tap):
    """tap-hubspot is a Singer tap for Hubspot."""

    name = "tap-hubspot"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "access_token",
            th.StringType,
            required=False,
            description="Token to authenticate against the API service",
        ),
        th.Property(
            "oauth_credentials",
            th.ObjectType(
                th.Property("client_id", th.StringType),
                th.Property("client_secret", th.StringType),
                th.Property("refresh_token", th.StringType),
            ),
            required=False,
            description="The OAuth credentials needed to authenticate against the API service.",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest record date to sync",
        ),
        th.Property(
            "end_date",
            th.DateTimeType,
            description="Latest record date to sync",
        ),
        th.Property(
            "extract_deal_associations",
            th.BooleanType,
            default=False,
            required=True,
            description="Enable the extraction of entities associated with deals",
        ),
        th.Property(
            "extract_deal_associations_comma_separated_string",
            th.StringType,
            required=False,
            default="calls, commerce_payments, communications, companies, contacts, deal_split, deals, emails, invoices, line_item, meetings, notes, orders, postal_mail, quotes, services, subscriptions, tasks, tickets",
            description="Comma separated string with the name of entities that should be extracted",
        ),
        th.Property(
            "extract_contact_associations",
            th.BooleanType,
            default=False,
            required=True,
            description="Enable the extraction of entities associated with contacts",
        ),
        th.Property(
            "extract_contact_associations_comma_separated_string",
            th.StringType,
            required=False,
            default="calls, communications, companies, contacts, emails, meetings, notes, subscriptions, tasks, tickets",
            description="Comma separated string with the name of entities that should be extracted",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.HubspotStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        streams_list = []

        custom_objects = self.get_custom_objects()
        for custom_object in custom_objects:
            user_logger.info(f"Discovered custom object: {custom_object['object_name']}")
            streams_list.append(
                streams.CustomObjectStream(
                    tap=self,
                    object_name=custom_object["object_name"],
                    object_qualified_name=custom_object["object_qualified_name"],
                    object_type_id=custom_object["object_type_id"],
                )
            )

        streams_list.extend(
            [
                streams.ContactStream(self),
                streams.UsersStream(self),
                streams.OwnersStream(self),
                streams.TicketPipelineStream(self),
                streams.DealPipelineStream(self),
                # streams.EmailSubscriptionStream(self),
                streams.PropertyNotesStream(self),
                streams.CompanyStream(self),
                streams.DealStream(self),
                # streams.FeedbackSubmissionsStream(self),
                streams.LineItemStream(self),
                streams.ProductStream(self),
                streams.TicketStream(self),
                streams.QuoteStream(self),
                # streams.GoalStream(self),
                streams.CallStream(self),
                streams.CommunicationStream(self),
                streams.EmailStream(self),
                streams.MeetingStream(self),
                streams.NoteStream(self),
                streams.PostalMailStream(self),
                streams.TaskStream(self),
            ]
        )

        return streams_list

    def get_custom_objects(self) -> list[dict]:
        """Get the custom objects from the Hubspot API."""
        endpoint = "https://api.hubapi.com/crm/v3/schemas"
        headers = {
            "Authorization": f"Bearer {self.get_access_token()}",
        }
        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            custom_objects = response.json()["results"]
            user_logger.info(f"Found {len(custom_objects)} custom objects")
            return [
                {
                    "object_name": custom_object["name"],
                    "object_qualified_name": custom_object["fullyQualifiedName"],
                    "object_type_id": custom_object["objectTypeId"],
                }
                for custom_object in custom_objects
            ]
        except Exception as e:
            user_logger.warning(f"Unable to get custom objects: {e}")
            return []

    def get_access_token(self) -> str:
        """Get the access token from the Hubspot API."""
        if self.config.get("access_token"):
            return self.config["access_token"]

        auth_url = "https://api.hubapi.com/oauth/v1/token"
        auth_payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.config["oauth_credentials"]["refresh_token"],
            "client_id": self.config["oauth_credentials"]["client_id"],
            "client_secret": self.config["oauth_credentials"]["client_secret"],
        }
        auth_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        try:
            auth_response = requests.post(auth_url, data=auth_payload, headers=auth_headers)
            auth_response.raise_for_status()
            return auth_response.json()["access_token"]
        except Exception as e:
            user_logger.error(f"Error getting access token: {e}")
            sys.exit(1)


if __name__ == "__main__":
    TapHubspot.cli()
