import httpx
import loguru

from app.application.interfaces.oauth_service import AbstractGoogleOAuthService, GoogleUserData
from app.infrastructure.config.config import config


class GoogleOAuthService(AbstractGoogleOAuthService):
    def __init__(self):
        self.client_id = config.google.google_client_id
        self.client_secret = config.google.google_secret_client_id

    async def get_user_data(self, code: str, redirect_uri: str) -> GoogleUserData:
        allowed_redirect_uris = config.google.allowed_redirect_uris
        if not allowed_redirect_uris:
            raise ValueError("Google redirect URI whitelist is not configured")
        if redirect_uri not in allowed_redirect_uris:
            raise ValueError("Unsupported redirect_uri")

        token_url = "https://oauth2.googleapis.com/token"
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            token_resp = await client.post(token_url, data=payload)
            if token_resp.status_code != 200:
                raise ValueError("Failed to exchange Google auth code")

            tokens_data = token_resp.json()
            access_token = tokens_data.get("access_token")

            user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            user_resp = await client.get(
                user_info_url,
                headers={"Authorization": f"Bearer {access_token}"},
            )

            if user_resp.status_code != 200:
                raise ValueError("Failed to fetch Google profile data")

            data = user_resp.json()
            loguru.logger.info("Google user data received successfully")

            if not data.get("email"):
                raise ValueError("Google did not return an email")

            return GoogleUserData(
                email=data.get("email"),
                google_id=data.get("id"),
                avatar_url=data.get("picture"),
                first_name=data.get("given_name"),
                last_name=data.get("family_name"),
            )
