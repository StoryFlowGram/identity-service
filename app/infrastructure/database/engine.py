from sqlalchemy.ext.asyncio import create_async_engine
from app.config.config import database_url


engine = create_async_engine(
    url=database_url(),
    echo=True
)