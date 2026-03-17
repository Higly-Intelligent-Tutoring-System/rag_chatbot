from langgraph.checkpoint.memory import InMemorySaver


async def get_checkpointer():
    """Returns a RAM-stored short-term memory"""
    checkpointer = InMemorySaver()
    return checkpointer