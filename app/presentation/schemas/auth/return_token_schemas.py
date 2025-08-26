from pydantic import BaseModel

class ReturnTokenSchema(BaseModel):
    access_token: str
    refresh_token: str