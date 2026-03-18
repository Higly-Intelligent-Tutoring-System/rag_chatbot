from contextlib import asynccontextmanager
from fastapi import FastAPI

from orchestrator.service import ChatService
from api.config import settings
from api.routes import router
from api.telemetry import init_telemetry

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup:  telemetry injection + create ChatService → attach to app.state
    Shutdown: close connections
    """
    init_telemetry()
    service = None  # TODO: create a method in wiring.py that returns the sevice.
    app.state.chat_service = service
    yield
    await service.close()


app = FastAPI(title="HITS Chatbot API", lifespan=lifespan)
app.include_router(router)