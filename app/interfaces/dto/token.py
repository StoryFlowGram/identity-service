from pydantic import BaseModel


class TokenDTO(BaseModel):
    sub: str
    exp: int
    iat: int
    
class TokenRefreshDTO(BaseModel):
    refresh_token: str

class TokenResponseDTO(BaseModel):
    access_token: str
    refresh_token: str