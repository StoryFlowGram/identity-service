from authlib.integrations.starlette_client import OAuthError

from app.interfaces.protocols.user_protocol import UserProtocol
from app.infrastructure.security.oauth import oauth_client_instance
from app.interfaces.dto.link_google import LinkGoogleDTO




class LinkGoogleEmailUseCase:
    def __init__(self, protocol: UserProtocol):
        self.protocol = protocol

    async def __call__(self, request, jwt_user_id: int):
        try: 
            token = await oauth_client_instance.google.authorize_access_token(request)
        
        except OAuthError as e:
            raise ValueError("Не удалось получить токен доступа от Google")
        
        user_info = token.get("userinfo", {})
        google_id = user_info.get("sub")
        email = user_info.get("email")
        if not google_id or not email:
            raise ValueError("Не удалось получить данные пользователя от Google")
        
        user = await self.protocol.get_by_id(jwt_user_id)
        if not user:
            raise ValueError("Пользователь не найден")
        
        linked = await self.protocol.update_google_account(
            user_id=jwt_user_id,
            google_id=google_id,
            email=email
        )

        return LinkGoogleDTO.from_domain(linked)