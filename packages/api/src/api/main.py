from contextlib import asynccontextmanager
from fastapi import FastAPI

from chatbot_orchestrator.service import ChatService
from api.wiring import build_chat_service
from api.routes import router
from api.telemetry import init_telemetry
from api.config import core_settings, api_settings

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup:  telemetry injection + create ChatService → attach to app.state
    Shutdown: close connections
    """
    init_telemetry(api_settings)
    service = build_chat_service(core_settings, api_settings)
    app.state.chat_service = service
    yield
    await service.close()


app = FastAPI(title="HITS Chatbot API", lifespan=lifespan)
app.include_router(router)