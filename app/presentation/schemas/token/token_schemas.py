from pydantic import BaseModel


class TokenSchema(BaseModel):
    sub: str
    exp: int
    iat: int


class TokenRefreshRequestSchema(BaseModel):
    refresh_token: str


class TokenRefreshResponseSchema(BaseModel):
    access_token: str
    refresh_token: str