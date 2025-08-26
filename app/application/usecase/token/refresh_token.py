from jwt import ExpiredSignatureError, PyJWTError
from loguru import logger

from app.domain.protocols.user_protocol import AbstractUserProtocol

from app.application.interfaces.token_service import AbstractJWTTokenService
from app.application.dto.token.token import TokenResponseDTO



class RefreshTokenUseCase:

    def __init__(self, protocol: AbstractUserProtocol, jwt_token_service: AbstractJWTTokenService) -> None:
        self.protocol = protocol
        self.jwt_token_service = jwt_token_service

    async def __call__(self, refresh_token: str) -> dict[str, str]:

        try:
            payload = self.jwt_token_service.get_user_id(refresh_token)

            if payload is None:
                raise ValueError("Пользователь не найден")

            new_token = self.jwt_token_service.create_token(payload)
            refresh_token = self.jwt_token_service.create_refresh_token(payload)

        except ExpiredSignatureError:
            raise ValueError("Refresh токен истёк")
        except PyJWTError:
            raise ValueError("Не валидный refresh токен")

        return TokenResponseDTO(
            access_token=new_token,
            refresh_token=refresh_token)
