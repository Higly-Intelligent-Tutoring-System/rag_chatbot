from typing import Literal

from .stores.postgres import get_store as get_postgres
from .stores.in_memory import get_store as get_memory


StoreType = Literal["postgres", "memory"]


async def get_store(store_type: StoreType = "memory", db_uri: str | None = None):
    match store_type:
        case "memory":
            return await get_memory()
        case "postgres":
            return await get_postgres(db_uri)
        case _:
            raise ValueError(f"Unsupported saver type: {store_type}")