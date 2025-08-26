from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True) 
class AuthGoogleDTO:
    access_token: str
    refresh_token: str
    user_id: int
    email: Optional[str] 
    first_name: Optional[str]
    last_name: Optional[str]
    avatar_url: Optional[str]
