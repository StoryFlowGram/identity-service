from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.infrastructure.config.config import config


def setup_proxy_middleware(app: FastAPI):
    trusted_hosts = config.security.trusted_hosts
    if not trusted_hosts:
        raise RuntimeError("TRUSTED_PROXY_HOSTS must contain at least one trusted host")
    app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=trusted_hosts)


def setup_session_middleware(app: FastAPI):
    app.add_middleware(
        SessionMiddleware,
        secret_key=config.session.secret_key,
        https_only=config.session.https_only,
        same_site=config.session.same_site,
    )
