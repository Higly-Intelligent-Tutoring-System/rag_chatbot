import asyncio
from .db import Base, engine
from . import models  # Ensures User is registered with Base

async def init_db(max_retries: int = 5) -> None:
    """Initialize database with retry logic for container startup delays."""
    for attempt in range(max_retries):
        try:
            print(f"🔄 Initializing database (attempt {attempt + 1}/{max_retries})...")
            async with engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)
            print("✅ Database initialized successfully")
            return
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"⚠️  Connection failed: {e}. Retrying in 2 seconds...")
                await asyncio.sleep(2)
            else:
                print(f"❌ Failed to initialize database after {max_retries} attempts")
                raise