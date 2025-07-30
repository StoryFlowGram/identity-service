from pydantic import BaseModel, Field
from typing import Optional

class UpdateProfileDTO(BaseModel):
    first_name: Optional[str] = Field(None, description="Имя пользователя")
    last_name: Optional[str] = Field(None, description="Фамилия пользователя")
    username: Optional[str] = Field(None, description="Имя пользователя в системе")
    avatar_url: Optional[str] = Field(None, description="URL аватара пользователя")