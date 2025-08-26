from pydantic import BaseModel, ConfigDict
from typing import Optional


class UpdateProfileSchema(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    avatar_url: Optional[str]

    model_config = ConfigDict(from_attributes=True)