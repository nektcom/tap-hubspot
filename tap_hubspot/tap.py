"""tap-hubspot tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers
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
            "client_id",
            th.StringType,
            required=False,
            description="The OAuth app client ID.",
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=False,
            description="The OAuth app client secret.",
        ),
        th.Property(
            "refresh_token",
            th.StringType,
            required=False,
            description="The OAuth app refresh token.",
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
    ).to_dict()

    def discover_streams(self) -> list[streams.HubspotStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [streams.DealStream(self)]

        return [
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


if __name__ == "__main__":
    TapHubspot.cli()
