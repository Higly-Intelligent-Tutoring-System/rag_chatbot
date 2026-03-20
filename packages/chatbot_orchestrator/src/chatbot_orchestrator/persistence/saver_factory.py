from typing import Literal

from .savers.postgres import get_checkpointer as get_postgres
from .savers.in_memory import get_checkpointer as get_memory


SaverType = Literal["postgres", "memory"]


async def get_checkpointer(saver_type: SaverType = "memory", db_uri: str | None = None):
    match saver_type:
        case "memory":
            return await get_memory()
        case "postgres":
            return await get_postgres(db_uri)
        case _:
            raise ValueError(f"Unsupported saver type: {saver_type}")