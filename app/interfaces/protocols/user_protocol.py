from abc import ABC, abstractmethod
from typing import Optional

from app.domain.User import User


class UserProtocol(ABC):

    @abstractmethod
    async def add(self, user: User):
        ...

    @abstractmethod
    async def get_by_telegram_id(self, tg_id: int):
        ...

    @abstractmethod
    async def get_by_google_id(self, google_id: str):
        ...

    @abstractmethod
    async def get_by_email(self, email: str):
        ...

    @abstractmethod
    async def update_profile(
        self, 
        user_id: int,
        first_name: str, 
        last_name: Optional[str], 
        username: Optional[str], 
        avatar_url: Optional[str]
        ):
        ...

    @abstractmethod
    async def update_google_account(
        self,
        user_id: int,
        google_id: str,
        email:str
        ):
        ...

    @abstractmethod
    async def delete(self, id_pk: int):
        ...

    