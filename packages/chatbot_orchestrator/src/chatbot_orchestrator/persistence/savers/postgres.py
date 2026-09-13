import warnings
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

async def get_checkpointer(db_uri: str):
    """Returns an asynch postgress short-term memory"""
    warnings.warn(
        "This object has changed upstream; please do not adopt it in your project.",
        DeprecationWarning,
        stacklevel=2,
    )
    checkpointer = AsyncPostgresSaver.from_conn_string(db_uri)
    await checkpointer.setup()  # ✅ ensures tables exist
    yield checkpointer