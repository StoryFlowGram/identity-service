import jwt
from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError, InvalidTokenError
from loguru import logger
from app.interfaces.dto.token import TokenDTO
from app.config.config import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

class SecurityService:
    @staticmethod
    def create_token(user_id: int):
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": user_id,
            "exp": expire,
            "iat": datetime.now(timezone.utc)
        }
        token =  jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
        logger.info(f"token: {token}")
        return token

    @staticmethod
    def create_refresh_token(user_id: int):
        expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {
            "sub": user_id,
            "exp": expire,
            "iat": datetime.now(timezone.utc)
        }
        token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
        logger.info(f"token: {token}")
        return token
    

    @staticmethod
    def decode_token(token: str):
        try: 
            payload = jwt.decode(
                token,
                JWT_SECRET,
                JWT_ALGORITHM,
                {"require_iat": True, "require_sub": True}
            )
            return TokenDTO(**payload)
        except ExpiredSignatureError:
            raise Exception("Token Истёк")
        except InvalidTokenError:
            raise Exception("Токен не валидный")