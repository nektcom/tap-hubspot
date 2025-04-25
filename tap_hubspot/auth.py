"""HubSpot Authentication."""

from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta


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
