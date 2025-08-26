from dataclasses import dataclass

@dataclass(frozen=True)
class TokenDTO:
    sub: str
    exp: int
    iat: int
    
@dataclass(frozen=True)
class TokenRefreshDTO:
    refresh_token: str

@dataclass(frozen=True)
class TokenResponseDTO:
    access_token: str
    refresh_token: str