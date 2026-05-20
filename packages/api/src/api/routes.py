from __future__ import annotations
from datetime import timedelta
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request, Response, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, field_validator

from chatbot_orchestrator.service import ChatService

from .db import get_db
from .auth import create_access_token, require_auth_dep, TokenResponse, verify_username_password_db
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
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
    ):
    username = await verify_username_password_db(db, form_data.username, form_data.password)
    access_token = create_access_token(subject=username, expires_delta=timedelta(seconds=api_settings.ACCESS_TOKEN_EXPIRE_SECONDS))
    return TokenResponse(access_token=access_token, expires_in=api_settings.ACCESS_TOKEN_EXPIRE_SECONDS)

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