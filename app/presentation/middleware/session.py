from app.config.config import SECRET_KEY
from starlette.middleware.sessions import SessionMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from fastapi import FastAPI


def setup_proxy_middleware(app: FastAPI):
    app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")


def setup_session_middleware(app: FastAPI):
    app.add_middleware(
        SessionMiddleware,
        secret_key=SECRET_KEY,
        https_only=False,
        same_site="lax",
    )