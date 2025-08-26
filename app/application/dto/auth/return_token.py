from dataclasses import dataclass


@dataclass(frozen=True)
class ReturnTokenDTO:
    access_token: str
    refresh_token: str