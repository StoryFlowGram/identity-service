from fastapi import APIRouter, Depends, HTTPException

from app.infrastructure.security.depends import get_user_protocol
from app.usecase.auth_via_telegram import AuthViaTelegramUsecase
from app.interfaces.dto.auth_telegram import AuthTelegramDTO, ReturnTokenDTO
from app.domain.User import User
from loguru import logger



user_router = APIRouter(prefix="/api/v1/user/auth", tags=["User"])



@user_router.post("/telegram")
async def auth_via_telegram(telegram_dto: AuthTelegramDTO, protocol = Depends(get_user_protocol)):
    usecase = AuthViaTelegramUsecase(protocol)
    try:
        created_telegram_user = await usecase(telegram_dto)
        return created_telegram_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
