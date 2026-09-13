import warnings
from langgraph.store.postgres.aio import AsyncPostgresStore

async def get_store(db_uri: str):
    """Returns a postgres long-term memory"""
    warnings.warn(
        "This object has changed upstream; please do not adopt it in your project.",
        DeprecationWarning,
        stacklevel=2,
    )
    store = AsyncPostgresStore.from_conn_string(db_uri)
    await store.setup()
    yield store