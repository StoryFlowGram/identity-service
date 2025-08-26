from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class ProfileResponseDTO:
    id: int
    telegram_id: Optional[int]
    google_id: Optional[str]
    email: Optional[str]
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    avatar_url: Optional[str]