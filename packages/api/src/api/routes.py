from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, field_validator

from chatbot_orchestrator.service import ChatService


# ── Dependency ──────────────────────────────────────────

def get_service(request: Request) -> ChatService:
    return request.app.state.chat_service


# ── Schemas ─────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    thread_id: str

    @field_validator("message", "thread_id")
    @classmethod
    def must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be empty")
        return value

class ChatResponseDTO(BaseModel):
    response: str
    thread_id: str


# ── Router ──────────────────────────────────────────────

router = APIRouter()


@router.post("/chat", response_model=ChatResponseDTO)
async def chat(
    req: ChatRequest,
    service: ChatService = Depends(get_service),
):
    result = await service.ainvoke(
        req.message,
        thread_id=req.thread_id,
    )
    return ChatResponseDTO(
        response=result,
        thread_id=req.thread_id,
    )

@router.get('/liveness')
async def liveness():
    return Response(content='{"message": "OK"}', media_type="application/json", status_code=200)