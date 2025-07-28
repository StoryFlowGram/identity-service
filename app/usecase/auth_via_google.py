# app/usecase/auth_via_google.py
from app.domain.User import User
from app.interfaces.protocols.user_protocol import UserProtocol
from app.infrastructure.security.security import SecurityService
from app.infrastructure.security.oauth import oauth_client_instance

class AuthViaGoogleUsecase:
    def __init__(self, protocol: UserProtocol):
        self.protocol = protocol

    async def __call__(self, request):

        token = await oauth_client_instance.google.authorize_access_token(request)
        if not token:
            raise ValueError("Не удалось получить токен доступа от Google")

        
        google_id = token.get("userinfo", {}).get("sub")
        email = token.get("userinfo", {}).get("email")
        first_name = token.get("userinfo", {}).get("given_name")
        last_name = token.get("userinfo", {}).get("family_name")
        avatar_url = token.get("userinfo", {}).get("picture")

        user = await self.protocol.get_by_google_id(google_id)
        if user is None:
            user = User(
                id=0,
                telegram_id=None,
                google_id=google_id,
                email=email,
                first_name=first_name,
                last_name=last_name,
                username=None,
                avatar_url=avatar_url
            )
            user = await self.protocol.add(user)

        access_token = SecurityService.create_token(user.id)
        refresh_token = SecurityService.create_refresh_token(user.id)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "google_id": user.google_id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "avatar_url": user.avatar_url
            }
        }
