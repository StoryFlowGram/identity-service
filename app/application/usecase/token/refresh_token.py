from jwt import ExpiredSignatureError, PyJWTError

from app.domain.protocols.user_protocol import AbstractUserProtocol
from app.application.interfaces.token_service import AbstractJWTTokenService
from app.application.dto.token.token import TokenResponseDTO


class RefreshTokenUseCase:

    def __init__(self, protocol: AbstractUserProtocol, jwt_token_service: AbstractJWTTokenService) -> None:
        self.protocol = protocol
        self.jwt_token_service = jwt_token_service

    async def __call__(self, refresh_token: str) -> dict[str, str]:
        try:
            payload = self.jwt_token_service.decode_token(refresh_token)
            if payload.get("type") != "refresh":
                raise ValueError("Invalid token type")

            user_id_raw = payload.get("sub")
            if user_id_raw is None:
                raise ValueError("Malformed refresh token")

            user_id = int(user_id_raw)
            token_version = int(payload.get("token_version", 0))

            user = await self.protocol.get_by_id(user_id)
            if user is None:
                raise ValueError("User not found")

            if user.token_version != token_version:
                raise ValueError("Refresh token revoked")

            new_token = self.jwt_token_service.create_token(
                user.id,
                user.telegram_id,
                user.token_version
            )
            new_refresh_token = self.jwt_token_service.create_refresh_token(
                user.id,
                user.token_version
            )
        except ExpiredSignatureError:
            raise ValueError("Refresh token expired")
        except PyJWTError:
            raise ValueError("Invalid refresh token")

        return TokenResponseDTO(
            access_token=new_token,
            refresh_token=new_refresh_token
        )
