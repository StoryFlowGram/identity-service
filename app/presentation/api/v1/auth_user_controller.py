from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from loguru import logger

from app.domain.protocols.user_protocol import AbstractUserProtocol
from app.application.interfaces.token_service import AbstractJWTTokenService
from app.application.usecase.auth.auth_via_google import AuthViaGoogleUsecase
from app.application.interfaces.oauth_service import AbstractOauthService
from app.application.usecase.auth.auth_via_telegram import AuthViaTelegramUsecase
from app.application.usecase.token.refresh_token import RefreshTokenUseCase
from app.presentation.schemas.auth.auth_telegram_schemas import AuthTelegramRequestSchema, AuthTelegramResponseSchema 
from app.presentation.schemas.token.token_schemas import TokenRefreshRequestSchema, TokenRefreshResponseSchema
from app.presentation.api.depends import get_oauth_service
from app.presentation.api.depends import get_user_protocol
from app.presentation.api.depends import get_jwt_token_service




auth_router = APIRouter(prefix="/api/v1/user/auth", tags=["Auth"])



@auth_router.post("/telegram", response_model=AuthTelegramResponseSchema)
async def auth_via_telegram(
    telegram_schema: AuthTelegramRequestSchema, 
    protocol = Depends(get_user_protocol), 
    jwt_token_service = Depends(get_jwt_token_service)
    ):
    usecase = AuthViaTelegramUsecase(protocol, jwt_token_service)
    try:
        created_telegram_user = await usecase(telegram_schema)
        return created_telegram_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@auth_router.get("/google")
async def login_via_google(request: Request, oauth_service: AbstractOauthService = Depends(get_oauth_service)):
    redirect_uri = request.url_for("auth_via_google")
    return await oauth_service.get_authorize_redirect(request, redirect_uri)
    


@auth_router.get("/callback/google")
async def auth_via_google(
    request: Request, protocol: AbstractUserProtocol = Depends(get_user_protocol), 
    get_jwt_token_service: AbstractJWTTokenService = Depends(get_jwt_token_service), 
    oauth_service: AbstractOauthService = Depends(get_oauth_service)):
    try:
        usecase = AuthViaGoogleUsecase(protocol, get_jwt_token_service, oauth_service)
        result = await usecase(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@auth_router.post("/refresh", response_model=TokenRefreshResponseSchema)
async def refresh_tokens(
    schema: TokenRefreshRequestSchema, 
    protocol: AbstractUserProtocol = Depends(get_user_protocol), 
    jwt_token_service: AbstractJWTTokenService = Depends(get_jwt_token_service)
    ):
    try:
        usecase = RefreshTokenUseCase(protocol, jwt_token_service)
        tokens = await usecase(schema.refresh_token)
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера {str(e)}")