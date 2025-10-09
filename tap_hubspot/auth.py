"""HubSpot Authentication."""

from nekt_singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta
from nekt_singer_sdk.helpers._util import utc_now
from typing_extensions import override


class HubSpotOAuthAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for HubSpot."""

    @property
    def oauth_request_body(self):
        return {
            "grant_type": "refresh_token",
            "client_id": self.config["oauth_credentials"]["client_id"],
            "client_secret": self.config["oauth_credentials"]["client_secret"],
            "refresh_token": self.config["oauth_credentials"]["refresh_token"],
        }

    @override
    def is_token_valid(self) -> bool:
        if self.last_refreshed is None:
            return False
        if not self.expires_in:
            return True
        return (self.expires_in - 60) > (
            utc_now() - self.last_refreshed
        ).total_seconds()  # anticipate 60 seconds to avoid race condition
