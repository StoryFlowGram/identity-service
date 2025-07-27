from app.domain.User import User
from app.interfaces.protocols.user_protocol import UserProtocol
from app.infrastructure.security.security import SecurityService
from app.interfaces.dto.auth_telegram import AuthTelegramDTO, ReturnTokenDTO

class AuthViaTelegramUsecase:
    def __init__(self, protocol: UserProtocol):
        self.protocol = protocol



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
        else:
            return user

        create_token = SecurityService.create_token(user.id)
        create_refresh_token = SecurityService.create_refresh_token(user.id)
        return {
            "access_token": create_token,
            "refresh_token": create_refresh_token,
            "user": user,
        }