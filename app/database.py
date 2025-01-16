from functools import cache
from typing import AsyncGenerator

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
)
from app.settings import get_settings

settings = get_settings()

database_url = f"{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"


@cache
def get_async_engine():
    return create_async_engine("postgresql+asyncpg://" + database_url, pool_size=3)


@cache
def get_general_session_maker(
    general_engine: AsyncEngine = Depends(get_async_engine),
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=general_engine, autoflush=False, autocommit=False)


async def get_general_session(
    general_session_maker: async_sessionmaker[AsyncSession] = Depends(
        get_general_session_maker
    ),
) -> AsyncGenerator[AsyncSession, None]:
    async with general_session_maker() as session:
        yield session
