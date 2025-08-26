from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AuthTelegramDTO:
    access_token: str
    refresh_token: str
    telegram_id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None