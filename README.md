# 🤖 HITS Chatbot Monorepository

Welcome to the monolithic repository for the RAG (Retrieval-Augmented Generation) Chatbot of the HITS project. This repository manages multiple Python components and a shared core library using **uv** workspaces to ensure consistent dependencies and versioning.

## 🏗️ Architecture

The project is structured as a Monorepo with the following components:

```text
rag-monorepo/
├── packages/
│   ├── core/                   # 🧠 Shared Library (Config, Database, Embeddings)
│   ├── document-loader/        # 📥 CLI Tool for Data Ingestion (Web & PDF)
│   ├── chatbot_orchestration/  # 🤖 Application layer (Chatbot engine)
│   ├── api/                    # ✉️ FastAPI Backend
│   ├── ui/                     # 🎓 Streamlit UI
│   └── evaluation/             # 📐 RAGAS evaluation engine
│
├── pyproject.toml              # Workspace Definition
├── uv.lock                     # Unified Lockfile
├── .env.dist                   # Environment template
└── ...                         # Other Configuration and Documentation
```

## ⚡ Prerequisites

- **Python**: 3.13 or higher
- **uv**: An extremely fast Python package installer and resolver.
  ```bash
  # Install uv (macOS/Linux)
  curl -LsSf https://astral.sh/uv/install.sh | sh
  
  # Install uv (Windows)
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

  For developers, it is recomended to use `ollama` as the LLM provider and use a local model to avoid wasting paid tokens from any remote provider.

  Moreover, even if all the project is runnable as detailed in the dedicated section below, adding a OCI compliant tool is highly suggested due to future deployment.


## 🚀 Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-org/rag-chatbot.git
    cd rag-chatbot
    ```

2.  **Sync the Workspace:**
    This command creates the virtual environment and installs dependencies for **all** packages in the workspace (Core, Loader, and API) simultaneously.
    ```bash
    uv sync --all-packages
    ```

3.  **Environment Configuration:**
    Create your local configuration file from the template.
    ```bash
    cp .env.dist .env
    ```

    Ideally up to 3 environments can be made:
    - **Developement (.dev)**: Confined to feature implementation and testing.
    - **Staging (.stg)**: Polished environment containing configuration for service separation at container level.
    - **Production (.prod)**: Final environment to be deplouyed, must be always valid.

    But in practice is important that it meets the needs of the moment.



## 📦 Packages Overview

**NOTE**: This is only a brief overview of the packages, please refer to the README.md you will find inside of each package for detailed documentation.

### 1. 🧠 Core (`packages/core`)
The foundation of the ecosystem. It is not an application itself but a library used by all other services.

*   **Responsibility**:
    *   **Configuration**: Manages Pydantic Settings and reads `.env`.
    *   **VectorDB Factory**: Provides a unified interface to get `Chroma` or `Supabase` clients.
    *   **Embeddings**: Centralizes the Embedding Model definition to ensure consistency between ingestion and retrieval.

### 2. 📥 Document Loader (`packages/document-loader`)
A Command Line Interface (CLI) tool responsible for populating the Vector Database.

*   **Features**:
    *   Recursive Web Crawling.
    *   PDF Text Extraction.
    *   Smart Chunking (rules defined in `core`).
    *   Batch processing.

*   **Usage**:
    ```bash
    # Crawl a website
    uv run --package document-loader python -m loader.main web "https://example.com"
    
    # Load a PDF
    uv run --package document-loader python -m loader.main pdf "./docs/manual.pdf"
    ```

    Check document_loader's `README.md` to know how to enable batch processing.

### 3. 🤖 Chatbot orchestrartor (`packages/chatbot_orchestrartor`)

The application layer of the HITS RAG chatbot.

This package contains the LangGraph-based conversational engine responsible for retrieval, generation, and conversation memory management. It is framework‑agnostic and designed to be consumed by the api package.


### 4. ✉️ FastAPI Backend (`packages/api`)

The web server layer of the HITS RAG chatbot.

This package exposes the framework-agnostic `chatbot_orchestrator` through RESTful HTTP endpoints using FastAPI. It acts as the bridge between client applications (UIs, external services) and the core conversational engine.

**Features**:
- **REST Endpoints**: Exposes the primary /chat endpoint for conversation and /liveness for infrastructure health checks.
- **Lifespan Management**: Safely handles application startup and shutdown, wiring the ChatService into the server state.
- **Observability**: Automatically initializes OpenTelemetry (e.g., Phoenix/Jaeger) tracing during server startup.
- **Data Validation**: Uses strict Pydantic models to validate incoming requests (e.g., preventing empty messages) and format responses.

Check the api's `README.md` for detailed usage documentation.


### 5. 🎓 Streamlit UI Package (`packages/ui`)

This package serves as the frontend layer of the smart tutoring system. It handles all user interactions, displays the conversational history, renders educational content (including code and math equations), and communicates with the backend tutoring engine (LLMs, RAG models, etc.) to generate personalized responses.


### 6. 📐 RAGAS evaluation engine (`packages/evaluation`)

Testing logic for the retrival and generation phases of the inference pipeline.
This package implements the RAGAS framework to evaluate overall application performance over the desired target responses it should ideally give out.

Most of the metrics implemented rely on the LLM-as-a-judge paradigm, therefore they are not deterministic and should not be interpreted as if they were.
These represent a useful benchmark to speed up the process by looking at the overall tendency of the system instead of single cases.

It should be kept in mind that this is a time-intensive procedure to apply and should not be abused in cost-sensitive environments.
The effectiveness of the tests are directly correlated to the capabilities of the LLM chosen as the judge.
Some tests will fail using a small local model, a way more advanced provider as OpenAI, Gemini or Claude is sincerely suggested.

Check the package's `README.md` for detailed documentation over the applied metrics.


## 🛠️ Development Workflow

### Running Tests
You can run tests for the entire monorepo or specific packages.

```bash
# Run ALL tests
uv run pytest

# Run tests for a specific package
uv run --package document-loader pytest
```

### Adding Dependencies
Because this is a workspace, you must specify which package receives the dependency.
In the examples below you will be guided to add a dependency only to the required one.

```bash
# Add 'pandas' to the document-loader only
uv add pandas --package document-loader

# Add 'httpx' to the shared core library
uv add httpx --package core
```

In case you added one by mistake, you can remove it by typing:

```bash
# Removes 'pandas' to the document-loader only
uv remove <lib> --package <package>
```