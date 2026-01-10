from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.infrastructure.database.session import get_session
from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.auth.jwt_service import JWTTokenService
from app.infrastructure.services.google_oauth_service import GoogleOAuthService



def get_jwt_token_service():
    return JWTTokenService()

async def get_user_protocol(session: AsyncSession = Depends(get_session)):
    return UserRepository(session)

async def get_oauth_service():
    return GoogleOAuthService()