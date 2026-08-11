from fastapi import APIRouter, Depends, HTTPException, status

from app.application.usecase.profile.delete_profile import DeleteProfileUseCase
from app.application.usecase.profile.update_profile_telegram import UpdateProfileUseCase
from app.presentation.api.depends import get_current_user, get_user_protocol
from app.presentation.schemas.profile.notification_settings_schema import (
    NotificationSettingsResponseSchema,
    UpdateNotificationSettingsSchema,
)
from app.presentation.schemas.profile.profile_schemas import ProfileSchema
from app.presentation.schemas.profile.update_profile_schemas import UpdateProfileSchema

profile_router = APIRouter(tags=["User"])


@profile_router.get("/me", response_model=ProfileSchema)
async def read_profile(
    user_id: int = Depends(get_current_user),
    protocol=Depends(get_user_protocol),
):
    user = await protocol.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Користувача не знайдено")
    return user


@profile_router.put("/me", response_model=dict)
async def update_profile(
    schema: UpdateProfileSchema,
    user_id: int = Depends(get_current_user),
    protocol=Depends(get_user_protocol),
):
    usecase = UpdateProfileUseCase(protocol)
    updated_user = await usecase(user_id, schema)
    return {"message": "Профіль оновлено", "user": updated_user}


@profile_router.patch("/me/notifications", response_model=NotificationSettingsResponseSchema)
async def update_notification_settings(
    schema: UpdateNotificationSettingsSchema,
    user_id: int = Depends(get_current_user),
    protocol=Depends(get_user_protocol),
):
    user = await protocol.update_notifications_enabled(user_id=user_id, enabled=schema.enabled)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Користувача не знайдено")
    return {"notifications_enabled": user.notifications_enabled}


@profile_router.delete("/me", response_model=dict)
async def delete_profile(
    user_id: int = Depends(get_current_user),
    protocol=Depends(get_user_protocol),
):
    usecase = DeleteProfileUseCase(protocol)
    await usecase(user_id)
    return {"message": "Профіль видалено"}
