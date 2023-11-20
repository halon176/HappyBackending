from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import NullPool

from src.config import settings as s

DATABASE_URL = f"postgresql+asyncpg://{s.db_user}:{s.db_pass.get_secret_value()}@{s.db_host}:{s.db_port}/{s.db_name}"


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
