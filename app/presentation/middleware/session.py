from app.infrastructure.config.config import config
from starlette.middleware.sessions import SessionMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from fastapi import FastAPI


def setup_proxy_middleware(app: FastAPI):
    app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")


def setup_session_middleware(app: FastAPI):
    app.add_middleware(
        SessionMiddleware,
        secret_key=config.session.secret_key,
        https_only=False,
        same_site="lax",
    )
