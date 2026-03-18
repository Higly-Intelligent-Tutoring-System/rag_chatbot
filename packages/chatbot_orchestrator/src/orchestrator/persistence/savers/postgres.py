from langgraph.checkpoint.postgres import AsyncPostgresSaver

async def get_checkpointer(db_uri: str):
    """Returns an asynch postgress short-term memory"""
    checkpointer = AsyncPostgresSaver.from_conn_string(db_uri)
    await checkpointer.setup()  # ✅ ensures tables exist
    return checkpointer