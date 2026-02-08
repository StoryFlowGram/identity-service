from fastapi import HTTPException, Header
from fastapi.security import HTTPBearer

bearer_scheme = HTTPBearer()

async def get_user_protocol():
    raise NotImplementedError("Должна быть реализация в Infra слое")

def get_jwt_token_service():
    raise NotImplementedError("Должна быть реализация в Infra слое")

def get_oauth_service():
    raise NotImplementedError("Должна быть реализация в Infra слое")


async def get_current_user(x_user_id: str = Header(None, alias="X-User-Id")) -> int:
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="X-User-Id заголовок отсутствует")
    if not x_user_id.isdigit():
        raise HTTPException(status_code=400, detail="X-User-Id не является числом")
    return int(x_user_id)