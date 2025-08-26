from pydantic import BaseModel
from typing import Optional


class LinkGoogleSchema(BaseModel):
    id: int
    telegram_id: Optional[int]
    google_id: Optional[str]
    email: str
    first_name: str
    last_name: str
    username: Optional[str]
    avatar_url: Optional[str]