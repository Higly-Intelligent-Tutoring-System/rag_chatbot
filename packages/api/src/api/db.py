# src/api/db.py
import os
from collections.abc import AsyncGenerator
from api.models import User
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import select

from .config import api_settings

DATABASE_URL = api_settings.postgres_db_uri()

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# Utility DB functions
async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    """Fetch a user by username. Returns None if not found."""
    q = select(User).where(User.username == username)
    result = await db.execute(q)
    return result.scalar_one_or_none()