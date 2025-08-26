from authlib.integrations.starlette_client import OAuth
from app.config.config import GOOGLE_CLIENT_ID, GOOGLE_SECRET_CLIENT_ID
from starlette.requests import Request
from dotenv import load_dotenv

from app.application.interfaces.oauth_service import AbstractOauthService

load_dotenv(override=True)


class GoogleOauthService(AbstractOauthService):
    def __init__(self):
        self.oauth_client_instance = OAuth()

        self.oauth_client_instance.register(
            name="google",
            client_id = GOOGLE_CLIENT_ID,
            client_secret= GOOGLE_SECRET_CLIENT_ID,
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={'scope': 'openid email profile',}
        )

    async def get_user_info(self, request: Request):
        token = await self.oauth_client_instance.google.authorize_access_token(request)
        if not token:
            raise ValueError("Не удалось получить токен доступа от Google")
        return token.get("userinfo", {})
    
    async def get_authorize_redirect(self, request: Request, redirect_uri: str):
        return await self.oauth_client_instance.google.authorize_redirect(request, redirect_uri)