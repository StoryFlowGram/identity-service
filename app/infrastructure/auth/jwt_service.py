import jwt
from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError, InvalidTokenError
from loguru import logger

from app.application.interfaces.token_service import AbstractJWTTokenService
from app.config.config import (
    JWT_SECRET,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)


class JWTTokenService(AbstractJWTTokenService):

    def __init__(self):
        self.secret = JWT_SECRET
        self.algorithm = JWT_ALGORITHM
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = REFRESH_TOKEN_EXPIRE_DAYS

    def create_token(self, user_id: int):
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "type": "access",
        }
        token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        logger.info(f"token: {token}")
        return token

    def create_refresh_token(self, user_id: int):
        expire = datetime.now(timezone.utc) + timedelta(days=self.refresh_token_expire_days)
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "type": "refresh",
        }
        token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        logger.info(f"token: {token}")
        return token

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
                options={"require_iat": True, "require_sub": True},
            )
            return payload
        except ExpiredSignatureError:
            raise Exception("Token истёк")
        except InvalidTokenError:
            raise Exception("Токен не валидный")

    def get_user_id(self, token: str) -> int:
        try:
            payload = self.decode_token(token)
            return int(payload["sub"])
        except Exception as e:
            logger.error(f"Ошибка при декодировании токена {e}")
            raise Exception("Невалидный токен")
