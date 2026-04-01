import os
import secrets

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPBearer

bearer_scheme = HTTPBearer()


async def get_user_protocol():
    raise NotImplementedError("Must be overridden in infra layer")


def get_jwt_token_service():
    raise NotImplementedError("Must be overridden in infra layer")


def get_oauth_service():
    raise NotImplementedError("Must be overridden in infra layer")


def _gateway_token() -> str:
    token = os.getenv("INTERNAL_GATEWAY_TOKEN")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="INTERNAL_GATEWAY_TOKEN is not configured",
        )
    return token


async def ensure_gateway_request(
    x_gateway_token: str | None = Header(default=None, alias="X-Gateway-Token"),
):
    expected_token = _gateway_token()
    if not x_gateway_token or not secrets.compare_digest(x_gateway_token, expected_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Request must come through trusted gateway",
        )


async def get_current_user(
    _: None = Depends(ensure_gateway_request),
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
) -> int:
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="X-User-Id header is missing")

    try:
        return int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="X-User-Id is not an integer")
