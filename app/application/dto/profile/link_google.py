from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class LinkGoogleDTO:
    id: int
    telegram_id: Optional[int]
    google_id: Optional[str]
    email: str
    first_name: str
    last_name: str
    username: Optional[str]
    avatar_url: Optional[str]
