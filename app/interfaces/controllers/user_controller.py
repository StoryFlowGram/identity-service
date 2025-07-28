from fastapi import APIRouter, Depends, HTTPException

from app.infrastructure.security.depends import get_user_protocol
from app.usecase.auth_via_telegram import AuthViaTelegramUsecase
from app.interfaces.dto.auth_telegram import AuthTelegramDTO, ReturnTokenDTO

from app.usecase.auth_via_google import AuthViaGoogleUsecase
from app.domain.User import User
from app.infrastructure.security.oauth import oauth_client_instance
from starlette.requests import Request
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

@user_router.get("/google")
async def login_via_google(request: Request):
    redirect_uri = request.url_for("auth_via_google")
    return await oauth_client_instance.google.authorize_redirect(request, redirect_uri)


@user_router.get("/callback/google")
async def auth_via_google(request: Request, protocol = Depends(get_user_protocol)):
    try:
        usecase = AuthViaGoogleUsecase(protocol)
        result = await usecase(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))