from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.config.config import config


def setup_cors(app: FastAPI):
    origins = config.security.cors_origins
    if not origins:
        raise RuntimeError("CORS_ALLOW_ORIGINS must contain at least one allowed origin")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
    )
