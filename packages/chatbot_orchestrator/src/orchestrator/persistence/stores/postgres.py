from langgraph.store.postgres.aio import AsyncPostgresStore
from orchestrator.config import DB_URI


async def get_store() -> AsyncPostgresStore:
    """Returns a postgres long-term memory"""
    store = AsyncPostgresStore.from_conn_string(DB_URI)
    await store.setup()
    return store