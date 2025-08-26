from abc import ABC, abstractmethod
from typing import Any

class AbstractOauthService(ABC):
    @abstractmethod
    async def get_user_info(self, access_token: str):
        raise NotImplementedError
    
    @abstractmethod
    async def get_authorize_redirect(self, request: Any, redirect_uri: str):
        raise NotImplementedError