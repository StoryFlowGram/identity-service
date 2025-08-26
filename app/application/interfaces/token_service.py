from abc import ABC, abstractmethod



class AbstractJWTTokenService(ABC):
    
    @abstractmethod
    def create_token(self, user_id: int):
        ...

    @abstractmethod
    def create_refresh_token(self, user_id: int):
        ...

    @abstractmethod
    def decode_token(self, token: str):
        ...

    @abstractmethod
    def get_user_id(self, token: str):
        ...
        