from loguru import logger
from app.domain.entities.user import User
from app.domain.protocols.user_protocol import AbstractUserProtocol
from app.application.interfaces.token_service import AbstractJWTTokenService
from app.application.interfaces.oauth_service import AbstractGoogleOAuthService
from app.application.dto.auth.auth_google import AuthGoogleDTO

class AuthViaGoogleUsecase:
    def __init__(self, protocol: AbstractUserProtocol, jwt_token_service: AbstractJWTTokenService, google_service: AbstractGoogleOAuthService):
        self.protocol = protocol
        self.jwt_token_service = jwt_token_service
        self.google_service = google_service

    async def __call__(self, code: str, redirect_uri: str) -> AuthGoogleDTO:

        try:
            user_info = await self.google_service.get_user_data(code, redirect_uri)
        except Exception as e:
            raise ValueError(f"Ошибка при получении данных о пользователе {str(e)}") 

        user = await self.protocol.get_by_google_id(user_info.google_id)
        if user is None: 
            new_user = User(
                id=0,
                telegram_id=None,
                google_id=user_info.google_id,
                email=user_info.email,
                first_name=user_info.first_name,
                last_name=user_info.last_name,
                username=user_info.email.split("@")[0],
                avatar_url=user_info.avatar_url
            )
            user = await self.protocol.add(new_user)
            logger.info(f"Создан новый пользователь через Google: {user.email} (ID: {user.id})")

        access_token = self.jwt_token_service.create_token(user.id)
        refresh_token = self.jwt_token_service.create_refresh_token(user.id)
        
        return AuthGoogleDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            avatar_url=user.avatar_url
        )
