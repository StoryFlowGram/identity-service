
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from loguru import logger
from dotenv import load_dotenv

from app.domain.protocols.user_protocol import AbstractUserProtocol
from app.application.interfaces.token_service import AbstractJWTTokenService
from app.application.usecase.auth.auth_via_google import AuthViaGoogleUsecase
from app.presentation.schemas.auth.auth_google_schemas import GoogleAuthCodeSchema

from app.application.usecase.auth.auth_via_telegram import AuthViaTelegramUsecase
from app.application.usecase.token.refresh_token import RefreshTokenUseCase
from app.presentation.schemas.auth.auth_telegram_schemas import  AuthResponseSchema, TelegramAuthRequest
from app.presentation.schemas.token.token_schemas import TokenRefreshResponseSchema
from app.presentation.schemas.auth.auth_google_schemas import  GoogleAuthCodeSchema
from app.presentation.api.depends import get_oauth_service
from app.presentation.api.depends import get_user_protocol
from app.presentation.api.depends import get_jwt_token_service



load_dotenv(override=False)

auth_router = APIRouter(tags=["Auth"])



@auth_router.post("/telegram", response_model=AuthResponseSchema)
async def auth_via_telegram(
    request: TelegramAuthRequest, 
    response: Response,
    protocol = Depends(get_user_protocol), 
    jwt_token_service = Depends(get_jwt_token_service)
):
    usecase = AuthViaTelegramUsecase(protocol, jwt_token_service)
    try:
        result = await usecase(request.initData)
        
        user = result.user 
        
        response.set_cookie(
            key="access_token", 
            value=result.access_token,
            httponly=True,
            samesite="none",
            secure=True,
            max_age=900
        )

        response.set_cookie(
            key="refresh_token", 
            value=result.refresh_token, 
            httponly=True,
            samesite="none",
            secure=True,
            max_age=14*24*60*60
        )
        
        return AuthResponseSchema(
            telegram_id=user.telegram_id,
            first_name=user.first_name,
            username=user.username
        )
    except ValueError as e:
        raise HTTPException(status_code=403, detail="Невірні дані від Telegram")

@auth_router.post("/google")
async def auth_via_google_popup(
    schema: GoogleAuthCodeSchema,
    response: Response,
    protocol: AbstractUserProtocol = Depends(get_user_protocol),
    jwt_token_service: AbstractJWTTokenService = Depends(get_jwt_token_service),
    google_service = Depends(get_oauth_service)
):
    usecase = AuthViaGoogleUsecase(protocol, jwt_token_service, google_service)
    try:
        auth_google_usecase = await usecase(schema.code, schema.redirect_uri)
        response.set_cookie(
            key="access_token", 
            value=auth_google_usecase.access_token,
            httponly=True,
            samesite="none",
            secure=True,    
            max_age=900
        )
        response.set_cookie(
            key="refresh_token",
            value=auth_google_usecase.refresh_token,
            httponly=True,
            samesite="none",
            secure=True,
            max_age=14*24*60*60
        )
        return auth_google_usecase
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера {str(e)}")
    

@auth_router.post("/refresh", response_model=TokenRefreshResponseSchema)
async def refresh_tokens(
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias="refresh_token"),
    protocol: AbstractUserProtocol = Depends(get_user_protocol), 
    jwt_token_service: AbstractJWTTokenService = Depends(get_jwt_token_service)
    ):
    if refresh_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Отсутствует refresh token в куках")
    try:
        usecase = RefreshTokenUseCase(protocol, jwt_token_service)
        tokens = await usecase(refresh_token)
        response.set_cookie(
            key="access_token", 
            value=tokens.access_token,
            httponly=True,
            samesite="none",
            secure=True,
            max_age=900
        )
        response.set_cookie(
            key="refresh_token",
            value=tokens.refresh_token,
            httponly=True,
            samesite="none",
            secure=True,
            max_age=14*24*60*60
        )
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера {str(e)}")
    


@auth_router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="access_token", httponly=True, samesite="none", secure=True)
    response.delete_cookie(key="refresh_token", httponly=True, samesite="none", secure=True)
    return {"status": "Logged out successfully"}