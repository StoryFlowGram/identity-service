from fastapi import FastAPI
from app.presentation.api.v1.auth_user_controller import auth_router 
from app.presentation.api.v1.profile_controller import profile_router
from app.presentation.api.v1.link_google_controller import link_google_router
from app.infrastructure.database.engine import engine
from app.infrastructure.database.base import Base
from app.presentation.middleware.cors import setup_cors
from app.presentation.middleware.session import setup_session_middleware
from app.presentation.api import depends
from app.infrastructure import di

app = FastAPI(title="identity-service")


setup_cors(app)
setup_session_middleware(app)

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(link_google_router)

app.dependency_overrides[depends.get_user_protocol] = di.get_user_protocol
app.dependency_overrides[depends.get_jwt_token_service] = di.get_jwt_token_service
app.dependency_overrides[depends.get_oauth_service] = di.get_oauth_service