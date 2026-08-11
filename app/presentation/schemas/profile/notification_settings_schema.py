from pydantic import BaseModel, ConfigDict


class UpdateNotificationSettingsSchema(BaseModel):
    enabled: bool

    model_config = ConfigDict(from_attributes=True)


class NotificationSettingsResponseSchema(BaseModel):
    notifications_enabled: bool

    model_config = ConfigDict(from_attributes=True)
