from pydantic import BaseModel
from typing import Optional


class GoogleAuthRequestSchema(BaseModel):
    user_id: int
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    avatar_url: Optional[str]


class GoogleAuthCodeSchema(BaseModel):
    code: str
    redirect_uri: str

