import httpx
import os

import loguru
from app.application.interfaces.oauth_service import AbstractGoogleOAuthService, GoogleUserData
from dotenv import load_dotenv

load_dotenv(override=False)

class GoogleOAuthService(AbstractGoogleOAuthService):
    def __init__(self):

        # проблема с env
        self.client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.client_secret = os.getenv("GOOGLE_SECRET_CLIENT_ID")


    async def get_user_data(self, code: str, redirect_uri: str) -> GoogleUserData:
        token_url = "https://oauth2.googleapis.com/token"
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }

        async with httpx.AsyncClient() as client:
            token_resp = await client.post(token_url, data=payload)
            if token_resp.status_code != 200:
                raise ValueError(f"Ошибка Google токена : {token_resp.text}")
            
            tokens_data = token_resp.json()
            access_token = tokens_data.get("access_token")

            user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
            user_resp = await client.get(
                user_info_url, 
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if user_resp.status_code != 200:
                raise ValueError("Не удалось получить данные профиля Google")

            data = user_resp.json()
            
            loguru.logger.info(f"Google user data: {data}")

            if not data.get("email"):
                 raise ValueError("Google не вернул Email")

            return GoogleUserData(
                email=data.get("email"),
                google_id=data.get("id"),
                avatar_url=data.get("picture"),
                first_name=data.get("given_name"),
                last_name=data.get("family_name")
            )