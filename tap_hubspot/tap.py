"""tap-hubspot tap class."""

from __future__ import annotations

import sys

import requests
from nekt_singer_sdk import typing as th
from nekt_singer_sdk.custom_logger import user_logger
from nekt_singer_sdk.tap_base import Tap
from tap_hubspot.client import HubspotStream
from tap_hubspot.streams import (
    CallStream,
    CommunicationStream,
    CompanyStream,
    ContactStream,
    CustomObjectStream,
    DealPipelineStream,
    DealStream,
    EmailStream,
    EmailSubscriptionStream,
    FeedbackSubmissionsStream,
    FormsStream,
    FormSubmissionsStream,
    GoalStream,
    LeadsStream,
    LineItemStream,
    MarketingEmailStream,
    MeetingStream,
    NoteStream,
    OwnersStream,
    PostalMailStream,
    ProductStream,
    PropertyNotesStream,
    QuoteStream,
    TaskStream,
    TicketPipelineStream,
    TicketStream,
    UsersStream,
)


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
        th.Property(
            "extract_ticket_associations",
            th.BooleanType,
            default=False,
            required=True,
            description="Enable the extraction of entities associated with tickets",
        ),
        th.Property(
            "extract_ticket_associations_comma_separated_string",
            th.StringType,
            required=False,
            default="calls, communications, companies, contacts, emails, meetings, notes, subscriptions, tasks",
            description="Comma separated string with the name of entities that should be extracted",
        ),
        th.Property(
            "extract_lead_associations",
            th.BooleanType,
            default=False,
            required=True,
            description="Enable the extraction of entities associated with leads",
        ),
        th.Property(
            "extract_lead_associations_comma_separated_string",
            th.StringType,
            required=False,
            default="calls, communications, companies, contacts, emails, meetings, notes, subscriptions, tasks, tickets",
            description="Comma separated string with the name of entities that should be extracted",
        ),
        th.Property(
            "extract_company_associations",
            th.BooleanType,
            default=False,
            required=True,
            description="Enable the extraction of entities associated with companies",
        ),
        th.Property(
            "extract_company_associations_comma_separated_string",
            th.StringType,
            required=False,
            default="calls, communications, companies, contacts, emails, meetings, notes, subscriptions, tasks",
            description="Comma separated string with the name of entities that should be extracted",
        ),
        th.Property(
            "extract_email_associations",
            th.BooleanType,
            default=False,
            required=True,
            description="Enable the extraction of entities associated with emails",
        ),
        th.Property(
            "extract_email_associations_comma_separated_string",
            th.StringType,
            required=False,
            default="companies, contacts, deals, tickets",
            description="Comma separated string with the name of entities that should be extracted",
        ),
        th.Property(
            "extract_contact_property_history",
            th.BooleanType,
            default=False,
            required=True,
            description="Enable the extraction of property history for contacts",
        ),
        th.Property(
            "extract_contact_property_history_comma_separated_string",
            th.StringType,
            required=False,
            default="lifecyclestage,lead_status",
            description="Comma separated string with the name of properties that should be extracted with history.",
        ),
        th.Property(
            "extract_deal_property_history",
            th.BooleanType,
            default=False,
            required=True,
            description="Enable the extraction of property history for deals",
        ),
        th.Property(
            "extract_deal_property_history_comma_separated_string",
            th.StringType,
            required=False,
            default="dealstage",
            description="Comma separated string with the name of properties that should be extracted with history.",
        ),
        th.Property(
            "enable_leads_stream",
            th.BooleanType,
            default=False,
            required=True,
            description="Enable the extraction of leads, only available for accounts with HubSpot Pro, Enterprise, or Enterprise Plus",
        ),
    ).to_dict()

    def discover_streams(self) -> list[HubspotStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        streams_list = []

        custom_objects = self.get_custom_objects()
        for custom_object in custom_objects:
            self.user_discovery_logger.info(f"Discovered custom object: {custom_object['object_name']}")
            streams_list.append(
                CustomObjectStream(
                    tap=self,
                    object_name=custom_object["object_name"],
                    object_qualified_name=custom_object["object_qualified_name"],
                    object_type_id=custom_object["object_type_id"],
                )
            )

        if self.config.get("enable_leads_stream"):
            streams_list.append(LeadsStream(self))

        streams_list.extend(
            [
                ContactStream(self),
                UsersStream(self),
                OwnersStream(self),
                TicketPipelineStream(self),
                DealPipelineStream(self),
                # EmailSubscriptionStream(self),
                PropertyNotesStream(self),
                CompanyStream(self),
                DealStream(self),
                # FeedbackSubmissionsStream(self),
                LineItemStream(self),
                ProductStream(self),
                TicketStream(self),
                QuoteStream(self),
                # GoalStream(self),
                CallStream(self),
                CommunicationStream(self),
                EmailStream(self),
                MeetingStream(self),
                NoteStream(self),
                PostalMailStream(self),
                TaskStream(self),
                FormsStream(self),
                FormSubmissionsStream(self),
                MarketingEmailStream(self),
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
            self.user_discovery_logger.info(f"Found {len(custom_objects)} custom objects")
            return [
                {
                    "object_name": custom_object["name"],
                    "object_qualified_name": custom_object["fullyQualifiedName"],
                    "object_type_id": custom_object["objectTypeId"],
                }
                for custom_object in custom_objects
            ]
        except Exception as e:
            self.user_discovery_logger.warning(f"Unable to get custom objects: {e}")
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
