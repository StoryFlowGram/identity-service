from pydantic import BaseModel


class TokenDTO(BaseModel):
    sub: int
    exp: int
    iat: int
    