from fastapi import APIRouter, Depends, HTTPException, Request

from app.presentation.api.depends import bearer_scheme, get_current_user, get_user_protocol
from app.application.interfaces.oauth_service import AbstractOauthService
from app.presentation.api.depends import get_oauth_service
from app.application.usecase.profile.link_google_email import LinkGoogleEmailUseCase
from app.presentation.api.depends import get_user_protocol


link_google_router = APIRouter(prefix="/api/v1/user/me", tags=["Link Google"])


@link_google_router.get("/login/google", dependencies=[Depends(bearer_scheme)])
async def link_google_login(request: Request, oauth_service: AbstractOauthService = Depends(get_oauth_service)):
    redirect_uri = request.url_for("callback")
    return await oauth_service.get_authorize_redirect(request, redirect_uri)

@link_google_router.get("/callback/link-google", name="callback", dependencies=[Depends(bearer_scheme)])
async def callback(
    request: Request, 
    user_id: int = Depends(get_current_user), 
    protocol = Depends(get_user_protocol),
    oauth_service: AbstractOauthService = Depends(get_oauth_service)
):
    try:
        usecase = LinkGoogleEmailUseCase(protocol, oauth_service)
        result = await usecase(request, user_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")