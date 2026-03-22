from pydantic import BaseModel
from typing import Optional

class TelegramAuthRequest(BaseModel):
    initData: str  


class AuthResponseSchema(BaseModel):
    telegram_id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
