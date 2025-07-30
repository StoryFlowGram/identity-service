from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from loguru import logger

from app.infrastructure.security.depends import get_user_protocol
from app.usecase.auth_via_telegram import AuthViaTelegramUsecase
from app.interfaces.dto.auth_telegram import AuthTelegramDTO
from app.usecase.auth_via_google import AuthViaGoogleUsecase
from app.infrastructure.security.oauth import oauth_client_instance
from app.interfaces.dto.token import TokenRefreshDTO
from app.usecase.refresh_token import RefreshTokenUseCase
from app.interfaces.dto.token import TokenResponseDTO




auth_router = APIRouter(prefix="/api/v1/user/auth", tags=["User"])



@auth_router.post("/telegram")
async def auth_via_telegram(telegram_dto: AuthTelegramDTO, protocol = Depends(get_user_protocol)):
    usecase = AuthViaTelegramUsecase(protocol)
    try:
        created_telegram_user = await usecase(telegram_dto)
        return created_telegram_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.get("/google")
async def login_via_google(request: Request):
    redirect_uri = request.url_for("auth_via_google")
    return await oauth_client_instance.google.authorize_redirect(request, redirect_uri)


@auth_router.get("/callback/google")
async def auth_via_google(request: Request, protocol = Depends(get_user_protocol)):
    try:
        usecase = AuthViaGoogleUsecase(protocol)
        result = await usecase(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@auth_router.post("/refresh", response_model=TokenResponseDTO)
async def refresh_tokens(dto: TokenRefreshDTO, protocol = Depends(get_user_protocol)):
    try:
        usecase = RefreshTokenUseCase(protocol)
        tokens = await usecase(dto.refresh_token)
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера {str(e)}")