from fastapi import APIRouter, Depends, HTTPException

from app.application.usecase.profile.link_google_email import LinkGoogleEmailUseCase
from app.infrastructure.di import get_oauth_service
from app.infrastructure.services.google_oauth_service import GoogleOAuthService
from app.presentation.api.depends import get_current_user
from app.presentation.api.depends import get_user_protocol
from app.domain.protocols.user_protocol import AbstractUserProtocol
from app.presentation.schemas.auth.auth_google_schemas import GoogleAuthCodeSchema


link_google_router = APIRouter(tags=["Link Google"])



@link_google_router.post("/link/google")
async def link_google_account(
    schema: GoogleAuthCodeSchema,
    user_id: int = Depends(get_current_user),
    protocol: AbstractUserProtocol = Depends(get_user_protocol),
    google_service: GoogleOAuthService = Depends(get_oauth_service)
):
    usecase = LinkGoogleEmailUseCase(protocol, google_service)
    
    try:
        result_dto = await usecase(
            user_id=user_id, 
            code=schema.code, 
            redirect_uri=schema.redirect_uri
        )
        return result_dto
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")