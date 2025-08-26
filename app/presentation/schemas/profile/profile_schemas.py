from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProfileSchema(BaseModel):
    id: int
    telegram_id: Optional[int]
    google_id: Optional[str]
    email: Optional[str]
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    avatar_url: Optional[str]

    model_config = ConfigDict(from_attributes=True)