from jwt import ExpiredSignatureError, PyJWTError

from app.interfaces.protocols.user_protocol import UserProtocol
from app.infrastructure.security.security import SecurityService
from app.interfaces.dto.token import TokenResponseDTO



class RefreshTokenUseCase:

    def __init__(self, protocol: UserProtocol) -> None:
        self.protocol = protocol

    async def __call__(self, refresh_token: str) -> dict[str, str]:
        try:
            payload = SecurityService.decode_token(refresh_token)
            user_id = int(payload.sub)

            if user_id is None:
                raise ValueError("Пользователь не найден")

            new_token = SecurityService.create_token(user_id)
            refresh_token = SecurityService.create_refresh_token(user_id)

        except ExpiredSignatureError:
            raise ValueError("Refresh токен истёк")
        except PyJWTError:
            raise ValueError("Не валидный refresh токен")

        return TokenResponseDTO(access_token=new_token, refresh_token=refresh_token)
