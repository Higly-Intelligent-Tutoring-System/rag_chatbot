from langgraph.checkpoint.postgres import AsyncPostgresSaver
from ...config import DB_URI


async def get_checkpointer():
    """Returns an asynch postgress short-term memory"""
    checkpointer = AsyncPostgresSaver.from_conn_string(
        DB_URI
    )
    await checkpointer.setup()  # ✅ ensures tables exist
    return checkpointer