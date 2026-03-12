from typing import Literal

from .stores.postgres import get_checkpointer as get_postgres
from .stores.in_memory import get_checkpointer as get_memory


SaverType = Literal["postgres", "memory"]


async def get_checkpointer(saver_type: SaverType = "memory"):
    match saver_type:
        case "memory":
            return await get_memory()
        case "postgres":
            return await get_postgres()
        case _:
            raise ValueError(f"Unsupported saver type: {saver_type}")