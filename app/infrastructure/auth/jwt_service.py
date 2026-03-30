import jwt
from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError, InvalidTokenError
from loguru import logger

from app.application.interfaces.token_service import AbstractJWTTokenService
from app.infrastructure.config.config import config


class JWTTokenService(AbstractJWTTokenService):

    def __init__(self):
        self.secret = config.jwt.jwt_secret
        self.algorithm = config.jwt.jwt_algorithm
        self.access_token_expire_minutes = config.jwt.access_token_expire_minutes
        self.refresh_token_expire_days = config.jwt.refresh_token_expire_days
        self.telegram_admin_id = config.jwt.telegram_admin_id

    def create_token(self, user_id: int, telegram_id: int | None = None, token_version: int = 0):
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
        role = "user"
        if telegram_id == self.telegram_admin_id:
            role = "admin"

        payload = {
            "sub": str(user_id),
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "role": role,
            "type": "access",
            "token_version": token_version,
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def create_refresh_token(self, user_id: int, token_version: int = 0):
        expire = datetime.now(timezone.utc) + timedelta(days=self.refresh_token_expire_days)
        payload = {
            "sub": str(user_id),
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "type": "refresh",
            "token_version": token_version,
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm],
                options={"require_iat": True, "require_sub": True},
            )
        except ExpiredSignatureError:
            logger.warning("Token expired")
            raise
        except InvalidTokenError:
            logger.warning("Invalid token")
            raise

    def get_user_id(self, token: str) -> int:
        payload = self.decode_token(token)
        sub = payload.get("sub")
        if sub is None:
            raise InvalidTokenError("Token missing subject")
        return int(sub)
