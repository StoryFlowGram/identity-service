from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    postgres_user: str = Field(alias="POSTGRES_USER")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(alias="POSTGRES_DB")
    db_name: str = Field(alias="DB_NAME")

    def get_database_url(self, DB_API: str) -> URL:
        return URL.create(
            drivername=f"postgresql+{DB_API}",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_db,
            database=self.db_name,
        )


class JWTConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    jwt_secret: str = Field(alias="JWT_SECRET")
    telegram_admin_id: int = Field(alias="TELEGRAM_ADMIN_ID")
    jwt_algorithm: str = Field(alias="JWT_ALGORITHM")
    refresh_token_expire_days: int = Field(alias="REFRESH_TOKEN_EXPIRE_DAYS")
    access_token_expire_minutes: int = Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES")


class SessionConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    secret_key: str = Field(alias="SECRET_KEY")


class GoogleOAuthConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    google_client_id: str = Field(alias="GOOGLE_CLIENT_ID")
    google_secret_client_id: str = Field(alias="GOOGLE_SECRET_CLIENT_ID")


class Config:
    def __init__(self):
        self.db = DatabaseConfig()
        self.jwt = JWTConfig()
        self.session = SessionConfig()
        self.google = GoogleOAuthConfig()


config = Config()


def database_url(DB_API: str) -> URL:
    return config.db.get_database_url(DB_API=DB_API)
