from pydantic import BaseModel, ConfigDict
from typing import Optional



class AuthGoogleDTO(BaseModel):
    access_token: str
    refresh_token: str
    user_id: int
    email: Optional[str] 
    first_name: Optional[str]
    last_name: Optional[str]
    avatar_url: Optional[str]

    model_config = ConfigDict(from_attributes=True)
