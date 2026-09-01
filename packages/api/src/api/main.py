from contextlib import asynccontextmanager
from fastapi import FastAPI

# ✅ Import models FIRST and EARLY to register them with Base
from . import models  # This ensures User is registered with Base
from chatbot_orchestrator.service import ChatService
from .wiring import build_chat_service
from .routes import router
from .telemetry import init_telemetry
from .init_db import init_db
from .config import core_settings, chatbot_settings, api_settings

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup:  telemetry injection + create ChatService → attach to app.state
    Shutdown: close connections
    """
    if api_settings.TELEMETRY_ENABLE:
        init_telemetry(api_settings)

    await init_db()
    
    service: ChatService = await build_chat_service(
        core_settings=core_settings, 
        chatbot_settings=chatbot_settings, 
        api_settings=api_settings
        )
    app.state.chat_service = service
    yield
    # await service.close()     TODO: Implement graceful shutdown


app = FastAPI(
    title="HITS Chatbot API", 
    lifespan=lifespan,
    docs_url="/docs" if api_settings.DOCS_ENABLED else None, 
    redoc_url="/redoc" if api_settings.DOCS_ENABLED else None,
    openapi_url="/openapi.json" if api_settings.DOCS_ENABLED else None,
)
app.include_router(router)

# TODO: Add rate limits and automated souspicius IP ban with fastap-guard