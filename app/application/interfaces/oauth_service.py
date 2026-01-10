from abc import ABC, abstractmethod
from pydantic import BaseModel

class GoogleUserData(BaseModel):
    email: str
    google_id: str
    first_name: str
    last_name: str | None = None
    avatar_url: str | None = None

class AbstractGoogleOAuthService(ABC):
    @abstractmethod
    async def get_user_data(self, code: str, redirect_uri: str) -> GoogleUserData:
        pass