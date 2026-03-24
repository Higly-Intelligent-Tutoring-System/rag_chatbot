from langgraph.store.postgres.aio import AsyncPostgresStore

async def get_store(db_uri: str) -> AsyncPostgresStore:
    """Returns a postgres long-term memory"""
    store = AsyncPostgresStore.from_conn_string(db_uri)
    await store.setup()
    return store