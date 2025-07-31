from fastapi import FastAPI
from app.interfaces.controllers.auth_user_controller import auth_router 
from app.interfaces.controllers.profile_controller import profile_router
from app.interfaces.controllers.link_google_controller import link_google_router
from app.infrastructure.database.engine import engine
from app.infrastructure.database.base import Base
from app.infrastructure.middleware.cors import setup_cors
from app.infrastructure.middleware.session import setup_session_middleware


app = FastAPI(title="identity-service")


setup_cors(app)
setup_session_middleware(app)

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(link_google_router)