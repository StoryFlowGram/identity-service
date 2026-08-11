from fastapi import APIRouter, Depends, HTTPException

from app.domain.protocols.user_protocol import AbstractUserProtocol
from app.presentation.api.depends import ensure_gateway_request, get_user_protocol


internal_router = APIRouter(tags=["Internal"])


@internal_router.get("/internal/users/{user_id}/token-version")
async def get_user_token_version(
    user_id: int,
    _: None = Depends(ensure_gateway_request),
    protocol: AbstractUserProtocol = Depends(get_user_protocol),
):
    user = await protocol.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "token_version": user.token_version}


@internal_router.get("/internal/users/{user_id}/telegram-id")
async def get_user_telegram_id(
    user_id: int,
    _: None = Depends(ensure_gateway_request),
    protocol: AbstractUserProtocol = Depends(get_user_protocol),
):
    user = await protocol.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "telegram_id": user.telegram_id}


@internal_router.get("/internal/users/{user_id}/notification-settings")
async def get_user_notification_settings(
    user_id: int,
    _: None = Depends(ensure_gateway_request),
    protocol: AbstractUserProtocol = Depends(get_user_protocol),
):
    user = await protocol.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "user_id": user_id,
        "telegram_id": user.telegram_id,
        "notifications_enabled": user.notifications_enabled,
    }
