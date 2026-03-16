from sqlalchemy.ext.asyncio import create_async_engine

from app.infrastructure.config.config import config


engine = create_async_engine(
    url=config.db.get_database_url(DB_API="asyncpg"),
    echo=True,
)