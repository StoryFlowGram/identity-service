from fastapi import FastAPI
from app.interfaces.controllers.user_controller import user_router
from app.infrastructure.database.engine import engine
from app.infrastructure.database.base import Base

app = FastAPI(title="identity-service")


app.include_router(user_router)