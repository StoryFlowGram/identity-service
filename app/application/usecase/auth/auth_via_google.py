from app.domain.entities.user import User
from app.domain.protocols.user_protocol import AbstractUserProtocol
from app.application.interfaces.token_service import AbstractJWTTokenService
from app.application.interfaces.oauth_service import AbstractOauthService
from app.application.dto.auth.auth_google import AuthGoogleDTO

class AuthViaGoogleUsecase:
    def __init__(self, protocol: AbstractUserProtocol, jwt_token_service: AbstractJWTTokenService, oauth_client_instance: AbstractOauthService):
        self.protocol = protocol
        self.jwt_token_service = jwt_token_service
        self.oauth_client_instance = oauth_client_instance

    async def __call__(self, request):

        user_info = await self.oauth_client_instance.get_user_info(request)

        google_id = user_info.get("sub")
        email = user_info.get("email")
        first_name = user_info.get("given_name")
        last_name = user_info.get("family_name")
        avatar_url = user_info.get("picture")

        user = await self.protocol.get_by_google_id(google_id)
        if user is None:
            user = User(
                id=0,
                telegram_id=None,
                google_id=google_id,
                email=email,
                first_name=first_name,
                last_name=last_name,
                username=None,
                avatar_url=avatar_url
            )
            user = await self.protocol.add(user)

        access_token = self.jwt_token_service.create_token(user.id)
        refresh_token = self.jwt_token_service.create_refresh_token(user.id)
        
        return AuthGoogleDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            avatar_url=user.avatar_url
        )
