# ✉️ HITS Chatbot API

FastAPI backend serving the HITS RAG Chatbot. This package is the **composition root** of the monorepo — it wires together `core` and `chatbot_orchestration`, handles authentication, and exposes REST endpoints.

## 🏗️ Architecture

```text
api/
└── src/
    └── api/
        ├── __init__.py
        ├── main.py              # FastAPI app + lifespan (wiring point)
        ├── config.py            # Aggregated config (reads env vars)
        ├── auth.py              # JWT authentication
        ├── routes/
        │   ├── __init__.py
        │   ├── chat.py          # POST /chat, POST /chat/stream
        │   ├── auth.py          # POST /login
        │   └── memory.py        # GET /memories, GET /history/{thread_id}
        └── schemas/
            ├── __init__.py
            └── http.py          # Request/Response DTOs
```

## Request flow

```
Client (Streamlit / curl / any HTTP client)
  │
  │  POST /chat  +  Bearer token  +  thread_id
  │
  ▼
┌─────────────────────────────────────────────┐
│  FastAPI                                    │
│                                             │
│  1. auth.py     → extract user_id from JWT  │
│  2. main.py     → get ChatService from      │
│                    app.state                │
│  3. routes/     → call service.ainvoke()    │
│                    passing user_id +        │
│                    thread_id                │
│                                             │
│  The API layer has ZERO knowledge of        │
│  LangGraph, prompts, or vector stores.      │
└─────────────────────────────────────────────┘
  │
  ▼
┌──────────────────────┐   ┌────────────────┐
│ chatbot_orchestration│   │     core       │
│ (graphs, nodes, LLM) │◄─►│  (retriever,   │
│                      │   │  embeddings)   │
└──────────────────────┘   └────────────────┘
```

## Run the webserver

```bash
(export $(cat .env.dev | xargs) && uv run uvicorn packages.api.src.api.main:app --reload)
```