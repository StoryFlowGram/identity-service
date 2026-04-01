from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


def _parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    user: str = Field(alias="IDENTITY_DB_USER")
    password: str = Field(alias="IDENTITY_DB_PASSWORD")
    db_name: str = Field(alias="IDENTITY_DB_NAME")
    host: str = Field(default="identity-db", alias="IDENTITY_DB_HOST")
    port: int = 5432

    def get_database_url(self, DB_API: str) -> URL:
        return URL.create(
            drivername=f"postgresql+{DB_API}",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db_name,
        )


class JWTConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    jwt_secret: str = Field(alias="GLOBAL_JWT_SECRET")
    telegram_admin_id: int = Field(alias="TELEGRAM_ADMIN_ID")
    jwt_algorithm: str = Field(alias="JWT_ALGORITHM")
    refresh_token_expire_days: int = Field(alias="REFRESH_TOKEN_EXPIRE_DAYS")
    access_token_expire_minutes: int = Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES")


class SessionConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    secret_key: str = Field(alias="GLOBAL_SECRET_KEY")
    https_only: bool = Field(default=True, alias="SESSION_HTTPS_ONLY")
    same_site: str = Field(default="lax", alias="SESSION_SAMESITE")


class GoogleOAuthConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    google_client_id: str = Field(alias="GOOGLE_CLIENT_ID")
    google_secret_client_id: str = Field(alias="GOOGLE_SECRET_CLIENT_ID")
    google_redirect_uri: str | None = Field(default=None, alias="GOOGLE_REDIRECT_URI")
    google_link_redirect_uri: str | None = Field(default=None, alias="GOOGLE_LINK_REDIRECT_URI")
    google_allowed_redirect_uris: str | None = Field(default=None, alias="GOOGLE_ALLOWED_REDIRECT_URIS")

    @property
    def allowed_redirect_uris(self) -> set[str]:
        configured = _parse_csv(self.google_allowed_redirect_uris)
        if configured:
            return set(configured)

        fallbacks = {
            uri
            for uri in [self.google_redirect_uri, self.google_link_redirect_uri]
            if uri
        }
        return fallbacks


class SecurityConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    internal_gateway_token: str = Field(alias="INTERNAL_GATEWAY_TOKEN")
    cors_allow_origins: str = Field(
        default="https://storyfluentgram.me,https://www.storyfluentgram.me",
        alias="CORS_ALLOW_ORIGINS",
    )
    trusted_proxy_hosts: str = Field(default="127.0.0.1", alias="TRUSTED_PROXY_HOSTS")

    @property
    def cors_origins(self) -> list[str]:
        return _parse_csv(self.cors_allow_origins)

    @property
    def trusted_hosts(self) -> list[str]:
        return _parse_csv(self.trusted_proxy_hosts)


class Config:
    def __init__(self):
        self.db = DatabaseConfig()
        self.jwt = JWTConfig()
        self.session = SessionConfig()
        self.google = GoogleOAuthConfig()
        self.security = SecurityConfig()


config = Config()


def database_url(DB_API: str) -> URL:
    return config.db.get_database_url(DB_API=DB_API)
