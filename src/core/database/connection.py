from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.settings.settings import settings

async_engine = create_async_engine(url=settings.DATABASE.dsn.unicode_string())
async_sessionmaker = async_sessionmaker(bind=async_engine, expire_on_commit=False)
