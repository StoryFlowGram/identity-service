from app.config.config import SECRET_KEY
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI


def setup_session_middleware(app: FastAPI):
    app.add_middleware(
        SessionMiddleware,
        secret_key=SECRET_KEY,
    )