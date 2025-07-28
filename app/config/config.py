import os
from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv(override=True)


def database_url():
    url = URL.create(
        drivername="postgresql+asyncpg",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
    )
    return url


JWT_SECRET = os.getenv("JWT_SECRET")
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_SECRET_CLIENT_ID = os.getenv("GOOGLE_SECRET_CLIENT_ID")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
