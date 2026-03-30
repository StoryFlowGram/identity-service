from jwt import PyJWTError
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status

from app.application.interfaces.token_service import AbstractJWTTokenService
from app.application.usecase.auth.auth_via_google import AuthViaGoogleUsecase
from app.application.usecase.auth.auth_via_telegram import AuthViaTelegramUsecase
from app.application.usecase.token.refresh_token import RefreshTokenUseCase
from app.domain.protocols.user_protocol import AbstractUserProtocol
from app.infrastructure.config.config import config
from app.presentation.api.depends import get_jwt_token_service
from app.presentation.api.depends import get_oauth_service
from app.presentation.api.depends import get_user_protocol
from app.presentation.schemas.auth.auth_google_schemas import GoogleAuthCodeSchema
from app.presentation.schemas.auth.auth_telegram_schemas import AuthResponseSchema, TelegramAuthRequest
from app.presentation.schemas.token.token_schemas import TokenRefreshResponseSchema


auth_router = APIRouter(tags=["Auth"])

ACCESS_COOKIE_MAX_AGE = config.jwt.access_token_expire_minutes * 60
REFRESH_COOKIE_MAX_AGE = config.jwt.refresh_token_expire_days * 24 * 60 * 60
COOKIE_OPTIONS = {
    "httponly": True,
    "samesite": "none",
    "secure": True,
    "path": "/",
}


def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=ACCESS_COOKIE_MAX_AGE,
        **COOKIE_OPTIONS,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=REFRESH_COOKIE_MAX_AGE,
        **COOKIE_OPTIONS,
    )


def clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(key="access_token", **COOKIE_OPTIONS)
    response.delete_cookie(key="refresh_token", **COOKIE_OPTIONS)


def get_user_id_from_token(jwt_token_service: AbstractJWTTokenService, token: str) -> int:
    payload = jwt_token_service.decode_token(token)
    sub = payload.get("sub")
    if sub is None:
        raise ValueError("Token does not contain subject")
    return int(sub)


@auth_router.post("/telegram", response_model=AuthResponseSchema)
async def auth_via_telegram(
    request: TelegramAuthRequest,
    response: Response,
    protocol: AbstractUserProtocol = Depends(get_user_protocol),
    jwt_token_service: AbstractJWTTokenService = Depends(get_jwt_token_service),
):
    usecase = AuthViaTelegramUsecase(protocol, jwt_token_service)
    try:
        result = await usecase(request.initData)
        user = result.user

        set_auth_cookies(response, result.access_token, result.refresh_token)

        return AuthResponseSchema(
            telegram_id=user.telegram_id,
            first_name=user.first_name,
            username=user.username,
        )
    except ValueError:
        raise HTTPException(status_code=403, detail="Невірні дані авторизації Telegram")


@auth_router.post("/google")
async def auth_via_google_popup(
    schema: GoogleAuthCodeSchema,
    response: Response,
    protocol: AbstractUserProtocol = Depends(get_user_protocol),
    jwt_token_service: AbstractJWTTokenService = Depends(get_jwt_token_service),
    google_service=Depends(get_oauth_service),
):
    usecase = AuthViaGoogleUsecase(protocol, jwt_token_service, google_service)
    try:
        auth_google_usecase = await usecase(schema.code, schema.redirect_uri)
        set_auth_cookies(response, auth_google_usecase.access_token, auth_google_usecase.refresh_token)
        return auth_google_usecase
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Помилка сервера: {str(exc)}")


@auth_router.post("/refresh", response_model=TokenRefreshResponseSchema)
async def refresh_tokens(
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias="refresh_token"),
    protocol: AbstractUserProtocol = Depends(get_user_protocol),
    jwt_token_service: AbstractJWTTokenService = Depends(get_jwt_token_service),
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token не знайдений",
        )

    try:
        usecase = RefreshTokenUseCase(protocol, jwt_token_service)
        tokens = await usecase(refresh_token)
        set_auth_cookies(response, tokens.access_token, tokens.refresh_token)
        return {"detail": "Токени успішно оновлено"}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Помилка сервера: {str(exc)}")


@auth_router.post("/logout")
async def logout_user(
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias="refresh_token"),
    access_token: str | None = Cookie(default=None, alias="access_token"),
    protocol: AbstractUserProtocol = Depends(get_user_protocol),
    jwt_token_service: AbstractJWTTokenService = Depends(get_jwt_token_service),
):
    token_to_revoke = refresh_token or access_token

    if token_to_revoke:
        try:
            user_id = get_user_id_from_token(jwt_token_service, token_to_revoke)
            await protocol.increment_token_version(user_id)
        except (ValueError, PyJWTError):
            pass

    clear_auth_cookies(response)
    return {"status": "Logged out"}
