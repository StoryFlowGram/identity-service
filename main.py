from fastapi import FastAPI
from app.interfaces.controllers.user_controller import user_router
from app.infrastructure.database.engine import engine
from app.infrastructure.database.base import Base
from app.infrastructure.middleware.cors import setup_cors
from app.infrastructure.middleware.session import setup_session_middleware


app = FastAPI(title="identity-service")


setup_cors(app)
setup_session_middleware(app)


app.include_router(user_router)