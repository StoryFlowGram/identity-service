from app.application.dto.auth.auth_telegram import AuthTelegramDTO
from app.domain.entities.User import User
from app.domain.protocols.user_protocol import AbstractUserProtocol
from app.application.interfaces.token_service import AbstractJWTTokenService
from app.infrastructure.auth.telegram_validator import validate_tma_init_data

import os
from loguru import logger


class AuthViaTelegramUsecase:
    def __init__(self, protocol: AbstractUserProtocol, jwt_token_service: AbstractJWTTokenService):
        self.protocol = protocol
        self.jwt_token_service = jwt_token_service

    async def __call__(self, init_data: str):
        bot_token = os.getenv("BOT_TOKEN") 
        validated_user_data = validate_tma_init_data(init_data, bot_token)
        
        telegram_id = validated_user_data.get("id")
        first_name = validated_user_data.get("first_name")
        last_name = validated_user_data.get("last_name")
        username = validated_user_data.get("username")

        user = await self.protocol.get_by_telegram_id(telegram_id)
        if user is None:
            user = User(
                id=0,
                telegram_id=telegram_id,
                google_id=None,
                email=None,
                first_name=first_name,
                last_name=last_name,
                username=username,
                avatar_url=None,
            )
            user = await self.protocol.add(user)

        access_token = self.jwt_token_service.create_token(user.id, user.telegram_id)
        refresh_token = self.jwt_token_service.create_refresh_token(user.id)
        
        return AuthTelegramDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user
        )