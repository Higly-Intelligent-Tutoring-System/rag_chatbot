from langgraph.store.memory import InMemoryStore

async def get_store():
    """Returns a RAM-stored long-term memory"""
    saver = InMemoryStore()
    return saver