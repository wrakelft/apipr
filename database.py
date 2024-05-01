from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import password, username, port, host, database_name

# from config import username, password, host, port, database_name


SQLALCHEMY_URL = f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database_name}"

engine = create_async_engine(SQLALCHEMY_URL)
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, autoflush=False, autocommit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
