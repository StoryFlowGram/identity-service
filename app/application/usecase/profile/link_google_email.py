from authlib.integrations.starlette_client import OAuthError

from app.domain.protocols.user_protocol import AbstractUserProtocol
from app.application.interfaces.oauth_service import AbstractOauthService
from app.application.dto.profile.link_google import LinkGoogleDTO




from authlib.integrations.starlette_client import OAuthError
from app.domain.protocols.user_protocol import AbstractUserProtocol
from app.application.interfaces.oauth_service import AbstractOauthService
from app.application.dto.profile.link_google import LinkGoogleDTO

class LinkGoogleEmailUseCase:
    def __init__(self, protocol: AbstractUserProtocol, oauth_service: AbstractOauthService):
        self.protocol = protocol
        self.oauth_service = oauth_service 

    async def __call__(self, request, jwt_user_id: int):
        try: 
            # Получаем информацию о пользователе через OAuth сервис
            user_info = await self.oauth_service.get_user_info(request)
        
        except OAuthError as e:
            raise ValueError(f"Не удалось получить токен доступа от Google: {str(e)}")
        
        google_id = user_info.get("sub")
        email = user_info.get("email")
        if not google_id or not email:
            raise ValueError("Не удалось получить данные пользователя от Google")
        
        user = await self.protocol.get_by_id(jwt_user_id)
        if not user:
            raise ValueError("Пользователь не найден")
        
        if user.google_id:
            raise ValueError("У вас уже привязан Google-аккаунт. Сначала отвяжите его.")
        
        check_google_id = await self.protocol.get_by_google_id(google_id)
        if check_google_id and check_google_id.id != user.id:
            raise ValueError("Указанный Google-аккаунт уже привязан к другому пользователю.")
        
        linked = await self.protocol.update_google_account(
            user_id=jwt_user_id,
            google_id=google_id,
            email=email
        )

        return LinkGoogleDTO(
            id=linked.id,
            telegram_id=linked.telegram_id,
            google_id=linked.google_id,
            email=linked.email,
            first_name=linked.first_name,
            last_name=linked.last_name,
            username=linked.username,
            avatar_url=linked.avatar_url
        )