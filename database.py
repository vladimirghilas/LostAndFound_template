from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncAttrs
from config import settings
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.async_database_url)
AsyncSessionLocal = async_sessionmaker(bind=engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
