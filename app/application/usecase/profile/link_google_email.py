from app.domain.protocols.user_protocol import AbstractUserProtocol
from app.application.interfaces.oauth_service import AbstractGoogleOAuthService
from app.application.dto.profile.link_google import LinkGoogleDTO

class LinkGoogleEmailUseCase:
    def __init__(
        self, 
        user_protocol: AbstractUserProtocol, 
        google_service: AbstractGoogleOAuthService
    ):
        self.user_protocol = user_protocol
        self.google_service = google_service

    async def __call__(self, user_id: int, code: str, redirect_uri: str) -> LinkGoogleDTO:
        try:
            google_user = await self.google_service.get_user_data(code, redirect_uri)
        except ValueError as e:
            raise ValueError(str(e))

        user = await self.user_protocol.get_by_id(user_id)
        if not user:
            raise ValueError("Пользователь не найден")

        if user.google_id:
            if user.google_id != google_user.google_id:
                 raise ValueError("У вас уже привязан другой Google-аккаунт.")

        existing_google_user = await self.user_protocol.get_by_google_id(google_user.google_id)
        if existing_google_user and existing_google_user.id != user.id:
            raise ValueError("Этот Google-аккаунт уже используется другим пользователем.")

        updated_user = await self.user_protocol.update_google_account(
            user_id=user.id,
            google_id=google_user.google_id,
            email=google_user.email
        )
        return LinkGoogleDTO(
            id=updated_user.id,
            telegram_id=updated_user.telegram_id,
            google_id=updated_user.google_id,
            email=updated_user.email,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            username=updated_user.username,
            avatar_url=updated_user.avatar_url
        )