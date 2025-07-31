from fastapi import APIRouter, Depends, HTTPException, Request

from app.infrastructure.security.depends import bearer_scheme, get_current_user, get_user_protocol
from app.infrastructure.security.oauth import oauth_client_instance
from app.usecase.link_google_email import LinkGoogleEmailUseCase
from app.interfaces.protocols.user_protocol import UserProtocol

link_google_router = APIRouter(prefix="/api/v1/user/me", tags=["Profile"])


@link_google_router.get("/login/google", dependencies=[Depends(bearer_scheme)])
async def link_google_login(request: Request):
    redirect_uri = request.url_for("callback")
    return await oauth_client_instance.google.authorize_redirect(request, redirect_uri)


@link_google_router.get("/callback/link-google", dependencies=[Depends(bearer_scheme)])
async def callback(request: Request, user_id: int = Depends(get_current_user), protocol: UserProtocol = Depends(get_user_protocol)):
    try:
        usecase = LinkGoogleEmailUseCase(protocol)
        result = await usecase(request, user_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера {str(e)}")