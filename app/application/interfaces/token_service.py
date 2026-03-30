from abc import ABC, abstractmethod



class AbstractJWTTokenService(ABC):
    
    @abstractmethod
    def create_token(self, user_id: int, telegram_id: int | None = None, token_version: int = 0):
        ...

    @abstractmethod
    def create_refresh_token(self, user_id: int, token_version: int = 0):
        ...

    @abstractmethod
    def decode_token(self, token: str):
        ...

    @abstractmethod
    def get_user_id(self, token: str):
        ...
        
