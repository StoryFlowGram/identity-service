from pydantic import BaseModel

class ReturnTokenDTO(BaseModel):
    access_token: str
    refresh_token: str