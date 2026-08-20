from chatbot_orchestrator.llms.llm_factory import LLMFactory

from chatbot_orchestrator import ChatService
from chatbot_orchestrator.graphs.registry import get_graph_builder 
from chatbot_orchestrator.persistence.saver_factory import get_checkpointer
from chatbot_orchestrator.persistence.store_factory import get_store
from core import get_vector_store
from .config import ApiSettings, ChatbotSettings, CoreSettings


async def build_chat_service(
        core_settings: CoreSettings,
        chatbot_settings: ChatbotSettings,
        api_settings: ApiSettings,
        ) -> ChatService:

    llm = LLMFactory.create(**chatbot_settings.llm_config.to_factory_kwargs())
    retriever = get_vector_store(core_settings)
    checkpointer = await get_checkpointer(api_settings.SAVER_BACKEND, api_settings.postgres_db_uri(checkpointer=True))
    store = await get_store(api_settings.STORER_BACKEND, api_settings.postgres_db_uri(checkpointer=True))
    
    # Build service
    service = ChatService(
        graph_builder=get_graph_builder(chatbot_settings.GRAPH_NAME),
        llm=llm,
        retriever=retriever,
        checkpointer=checkpointer,
        store=store,
    )

    # compile graph
    await service.compile()

    return service