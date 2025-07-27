from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.session import get_session
from app.infrastructure.repositories.user_repository import UserRepository

async def get_user_protocol(session: AsyncSession = Depends(get_session)):
    return UserRepository(session)
