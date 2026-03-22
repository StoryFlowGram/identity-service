from dataclasses import dataclass
from app.domain.entities.User import User


@dataclass(frozen=True)
class AuthTelegramDTO:
    access_token: str
    refresh_token: str
    user: User