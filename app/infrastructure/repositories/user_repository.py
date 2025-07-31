from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.interfaces.protocols.user_protocol import UserProtocol
from app.infrastructure.models.user_models import User as UserModel
from app.domain.User import User as DomainUser


class UserRepository(UserProtocol):
    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    async def add(self, user: DomainUser):
        orm = UserModel(
            telegram_id=user.telegram_id,
            google_id=user.google_id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            avatar_url=user.avatar_url

        )
        self.session_factory.add(orm)
        await self.session_factory.commit()
        await self.session_factory.refresh(orm)
        return DomainUser(
            id=orm.id,
            telegram_id=orm.telegram_id,
            google_id=orm.google_id,
            email=orm.email,
            first_name=orm.first_name,
            last_name=orm.last_name,
            username=orm.username,
            avatar_url=orm.avatar_url
        )
    
    async def get_by_telegram_id(self, tg_id: int):
        stmt = select(UserModel).where(UserModel.telegram_id == tg_id)
        result = await self.session_factory.execute(stmt)
        orm = result.scalars().one_or_none()
        if not orm:
            return None
        return DomainUser(
            id=orm.id,
            telegram_id=orm.telegram_id,
            google_id=orm.google_id,
            email=orm.email,
            first_name=orm.first_name,
            last_name=orm.last_name,
            username=orm.username,
            avatar_url=orm.avatar_url
        )
    
    async def get_by_email(self, email: str):
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session_factory.execute(stmt)
        orm = result.scalars().first()
        if not orm:
            return None
        
        return DomainUser(
            id=orm.id,
            telegram_id=orm.telegram_id,
            google_id=orm.google_id,
            email=orm.email,
            first_name=orm.first_name,
            last_name=orm.last_name,
            username=orm.username,
            avatar_url=orm.avatar_url
        )
        
    async def get_by_id(self, id_pk):
        stmt = select(UserModel).where(UserModel.id == id_pk)
        result = await self.session_factory.execute(stmt)
        orm = result.scalars().first()
        if not orm:
            return None
        
        return DomainUser(
            id=orm.id,
            telegram_id=orm.telegram_id,
            google_id=orm.google_id,
            email=orm.email,
            first_name=orm.first_name,
            last_name=orm.last_name,
            username=orm.username,
            avatar_url=orm.avatar_url
        )

    async def get_by_google_id(self, google_id: str):
        stmt = select(UserModel).where(UserModel.google_id == google_id)
        result = await self.session_factory.execute(stmt)
        orm = result.scalars().first()
        if not orm:
            return None
    
        return DomainUser(
            id=orm.id,
            telegram_id=orm.telegram_id,
            google_id=orm.google_id,
            email=orm.email,
            first_name=orm.first_name,
            last_name=orm.last_name,
            username=orm.username,
            avatar_url=orm.avatar_url
        )
    
    async def update_profile(self, user_id: int, first_name: str, last_name: Optional[str], username: Optional[str], avatar_url: Optional[str]):
        stmt = update(UserModel).where(UserModel.id == user_id).values(
            first_name=first_name, last_name=last_name, username=username, avatar_url=avatar_url
        )
        await self.session_factory.execute(stmt)
        await self.session_factory.commit()
        
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session_factory.execute(stmt)
        orm = result.scalars().one()
        
        return DomainUser(
            id=orm.id,
            telegram_id=orm.telegram_id,
            google_id=orm.google_id,
            email=orm.email,
            first_name=orm.first_name,
            last_name=orm.last_name,
            username=orm.username,
            avatar_url=orm.avatar_url
        )
    
    async def update_google_account(self, user_id: int, google_id: str, email:str):
        stmt = update(UserModel).where(UserModel.id == user_id).values(
            google_id=google_id, email=email
        )
        result = await self.session_factory.execute(stmt)
        await self.session_factory.commit()
        stmt_select = select(UserModel).where(UserModel.id == user_id)
        result = await self.session_factory.execute(stmt_select)
        orm = result.scalars().one()
        return DomainUser(
            orm.id,
            orm.telegram_id,
            orm.google_id,
            orm.email,
            orm.first_name,
            orm.last_name,
            orm.username,
            orm.avatar_url 
        )
    
    async def delete(self, id_pk: int):
        stmt = delete(UserModel).where(UserModel.id == id_pk)
        await self.session_factory.execute(stmt)
        await self.session_factory.commit()