import logging

from fastapi import APIRouter, Depends, HTTPException

from app.application.usecase.profile.link_google_email import LinkGoogleEmailUseCase
from app.domain.protocols.user_protocol import AbstractUserProtocol
from app.infrastructure.di import get_oauth_service
from app.infrastructure.services.google_oauth_service import GoogleOAuthService
from app.presentation.api.depends import get_current_user, get_user_protocol
from app.presentation.schemas.auth.auth_google_schemas import GoogleAuthCodeSchema


link_google_router = APIRouter(tags=["Link Google"])
logger = logging.getLogger(__name__)


@link_google_router.post("/link/google")
async def link_google_account(
    schema: GoogleAuthCodeSchema,
    user_id: int = Depends(get_current_user),
    protocol: AbstractUserProtocol = Depends(get_user_protocol),
    google_service: GoogleOAuthService = Depends(get_oauth_service),
):
    usecase = LinkGoogleEmailUseCase(protocol, google_service)

    try:
        return await usecase(
            user_id=user_id,
            code=schema.code,
            redirect_uri=schema.redirect_uri,
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Failed to link Google account")
    except Exception:
        logger.exception("Unexpected error while linking Google account for user %s", user_id)
        raise HTTPException(status_code=500, detail="Internal server error")
