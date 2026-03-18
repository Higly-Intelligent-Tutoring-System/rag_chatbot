# api/wiring.py

from langchain.chat_models import init_chat_model 

from chatbot_orchestrator import ChatService
# from chatbot_orchestration.graphs.rag_graph import build_rag_graph
# from chatbot_orchestration.persistence.saver_factory import create_checkpointer
# from chatbot_orchestration.persistence.store_factory import create_store

from core import get_retriever

from .config import settings


async def build_chat_service() -> ChatService:
    # LLM
    llm = init_chat_model(
        model=settings.MODEL_NAME,
        model_provider=settings.MODEL_PROVIDER,
        temperature=0,
    )

    # Retriever
    retriever = get_retriever()

    # Conversation saver
    checkpointer = None     # TODO: Create saver.

    # Optional store
    store = None
    if settings.STORE_BACKEND:
        store = None        # TODO: Create saver.
    # Build service
    service = ChatService(
        graph_builder=None, # TODO: Use graph builder.
        llm=llm,
        retriever=retriever,
        checkpointer=checkpointer,
        store=store,
    )

    # compile graph
    service.compile()

    return service