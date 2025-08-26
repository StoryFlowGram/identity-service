from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class UpdateProfileDTO:
    first_name: Optional[str] 
    last_name: Optional[str]
    username: Optional[str] 
    avatar_url: Optional[str]