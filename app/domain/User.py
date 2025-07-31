from dataclasses import dataclass
from typing import Optional



@dataclass(slots=True, frozen=True)
class User:
    id: int
    telegram_id: Optional[int]
    google_id: Optional[str]
    email: Optional[str]
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    avatar_url: Optional[str]
