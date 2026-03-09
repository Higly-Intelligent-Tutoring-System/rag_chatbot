# 🤖 Chatbot Orchestration Package

This package contains the **RAG orchestration logic** for the HITS Chatbot.

It is responsible for:

- Managing conversations
- Injecting message history using `MessagesPlaceholder`
- Executing the RAG pipeline
- Coordinating persistence
- Async execution support

---

## 🏗️ Architecture Role

This package represents the **Application Layer**.

It orchestrates:

- ✅ Vector retrieval (via `core`)
- ✅ LLM calls (LangChain or LangGraph)
- ✅ Persistence
- ✅ Conversation injection
- ✅ Telemetry tracing


---

## 🧠 RAG Design

The RAG chain:
```
    ┌─────────────────────────┐
    │   Initial User Query    │
    └────────────┬────────────┘
                 │
                 ↓
┌─────────────────────────────────────┐
│          Memory retrival            │
│     (full conversation history)     │
└────────────────┬────────────────────┘
                 │
                 ├───────────────────────────────────┐
                 │                                   |
                 ↓                                   |
┌─────────────────────────────────────┐              |
│         Context Injection           │              |
│         (vector retriever)          │              |
└────────────────┬────────────────────┘              |
                 │                                   |
                 ↓                                   |
        ┌─────────────────┐                 ┌────────┴────────┐
        │      Agent      │                 │      Query      │
        └────────┬────────┘                 └─────────────────┘
                 │                                   ↑
                 ↓                                   |
        ┌─────────────────┐                 ┌────────┴────────┐
        │  String Output  │                 │       User      │
        └────────┬────────┘                 └─────────────────┘
                 │                                   ↑
                 └───────────────────────────────────┘
```