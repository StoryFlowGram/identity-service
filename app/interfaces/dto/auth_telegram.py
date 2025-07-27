from pydantic import BaseModel, ConfigDict
from typing import Optional


class AuthTelegramDTO(BaseModel):
    telegram_id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ReturnTokenDTO(BaseModel):
    access_token: str
    refresh_token: str