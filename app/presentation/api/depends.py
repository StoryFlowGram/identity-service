from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jwt import InvalidTokenError, ExpiredSignatureError
from loguru import logger


from app.application.interfaces.token_service import AbstractJWTTokenService

bearer_scheme = HTTPBearer()

async def get_user_protocol():
    raise NotImplementedError("Должна быть реализация в Infra слое")

def get_jwt_token_service():
    raise NotImplementedError("Должна быть реализация в Infra слое")

def get_oauth_service():
    raise NotImplementedError("Должна быть реализация в Infra слое")


def get_current_user(
    token: str = Depends(bearer_scheme), 
    token_service: AbstractJWTTokenService = Depends(get_jwt_token_service)
):
    jwt_token = token.credentials
    try: 
        user_id = token_service.get_user_id(jwt_token)
        return user_id
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Токен истёк",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Токен не валидный",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        logger.error(f"Ошибка при проверке токена: {e}")
        raise HTTPException(
            status_code=401,
            detail="Невалидный токен",
            headers={"WWW-Authenticate": "Bearer"}
        )