from __future__ import annotations
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, field_validator

from chatbot_orchestrator.service import ChatService

from .auth import create_access_token, require_auth_dep, verify_username_password, TokenResponse
from .config import api_settings


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

@router.post("/token", response_model=TokenResponse)
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if not verify_username_password(form_data.username, form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    access_token = create_access_token(subject=form_data.username, expires_delta=None)
    return TokenResponse(access_token=access_token, expires_in=api_settings.access_token_expire_seconds)

@router.post("/chat", response_model=ChatResponseDTO)
async def chat(
    req: ChatRequest,
    service: Annotated[ChatService, Depends(get_service)],
    _user: Annotated[str | None, Depends(require_auth_dep)],
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