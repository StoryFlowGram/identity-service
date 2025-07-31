from pydantic import BaseModel
from typing import Optional


class LinkGoogleDTO(BaseModel):
    id: int
    telegram_id: Optional[int]
    google_id: Optional[str]
    email: str
    first_name: str
    last_name: str
    username: Optional[str]
    avatar_url: Optional[str]

    @classmethod
    def from_domain(cls, user):
        return cls(
            id=user.id,
            telegram_id=user.telegram_id,
            google_id=user.google_id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            avatar_url=user.avatar_url
        )