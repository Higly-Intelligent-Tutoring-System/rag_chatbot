from langchain.chat_models import init_chat_model 

from chatbot_orchestrator import ChatService
from chatbot_orchestrator.graphs.registry import get_graph_builder 
from chatbot_orchestrator.persistence.saver_factory import get_checkpointer
from chatbot_orchestrator.persistence.store_factory import get_store
from core import get_vector_store
from .config import ApiSettings, CoreSettings


async def build_chat_service(
        core_settings: CoreSettings, 
        api_settings: ApiSettings
        ) -> ChatService:
    
    llm = init_chat_model(
        model=api_settings.MODEL_NAME,
        model_provider=api_settings.PROVIDER_NAME,
        temperature=api_settings.MODEL_TEMPERATURE,
    )
    retriever = get_vector_store(core_settings)
    checkpointer = await get_checkpointer(api_settings.SAVER_BACKEND, api_settings.postgres_db_uri(checkpointer=True))
    store = await get_store(api_settings.STORER_BACKEND, api_settings.postgres_db_uri(checkpointer=True))
    
    # Build service
    service = ChatService(
        graph_builder=get_graph_builder(api_settings.GRAPH_NAME),
        llm=llm,
        retriever=retriever,
        checkpointer=checkpointer,
        store=store,
    )

    # compile graph
    await service.compile()

    return service