from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer
from jwt import InvalidTokenError, ExpiredSignatureError
from loguru import logger

from app.infrastructure.database.session import get_session
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.security.security import SecurityService

bearer_scheme = HTTPBearer()

async def get_user_protocol(session: AsyncSession = Depends(get_session)):
    return UserRepository(session)

def get_current_user(token: str = Depends(bearer_scheme)):
    jwt_token = token.credentials
    try: 
        payload = SecurityService.decode_token(jwt_token)
        return int(payload.sub)
    
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