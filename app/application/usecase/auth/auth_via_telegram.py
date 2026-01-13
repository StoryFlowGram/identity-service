from app.domain.entities import User
from app.domain.protocols.user_protocol import AbstractUserProtocol
from app.application.interfaces.token_service import AbstractJWTTokenService
from app.application.dto.auth.auth_telegram import AuthTelegramDTO

class AuthViaTelegramUsecase:
    def __init__(self, protocol: AbstractUserProtocol, jwt_token_service: AbstractJWTTokenService):
        self.protocol = protocol
        self.jwt_token_service = jwt_token_service



    async def __call__(self, telegram_dto: AuthTelegramDTO):
        user = await self.protocol.get_by_telegram_id(telegram_dto.telegram_id)
        if user is None:
            user = User(
                id=0,
                telegram_id=telegram_dto.telegram_id,
                google_id=None,
                email=None,
                first_name=telegram_dto.first_name,
                last_name=telegram_dto.last_name,
                username=telegram_dto.username,
                avatar_url=None,
            )
            user = await self.protocol.add(user)

        create_token = self.jwt_token_service.create_token(user.id, user.telegram_id)
        create_refresh_token = self.jwt_token_service.create_refresh_token(user.id)
        return AuthTelegramDTO(
            access_token=create_token,
            refresh_token=create_refresh_token,
            telegram_id=user.telegram_id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username
        )