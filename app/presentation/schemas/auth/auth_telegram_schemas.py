from pydantic import BaseModel
from typing import Optional


class AuthTelegramSchema(BaseModel):
    telegram_id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
