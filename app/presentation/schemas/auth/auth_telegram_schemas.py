from pydantic import BaseModel
from typing import Optional


class AuthTelegramResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    telegram_id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None


class AuthTelegramRequestSchema(BaseModel):
    telegram_id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None