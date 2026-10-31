## 👁️ Project Vision

HITS promotes positive digital behaviours in teaching and learning through personal growth, a digital mindset, and targeted, technology-enabled interventions. It aims to strengthen motivation, willingness, and autonomy, moving beyond predicting behaviour to supporting meaningful change in how digital tools are used.

As part of this approach, HITS offers a tailored chatbot for students, built on the project’s core principles. The chatbot supports students in developing digital-friendly learning habits and greater autonomy, and provides grounded answers based on its built-in knowledge base. HITS also draws on Nudge Theory to encourage better digital education practices and Participatory Action Research to involve people in shaping and improving the project.

## 📦 Packages Overview

**NOTE**: This is only a brief overview of the packages, please refer to the README.md you will find inside of each package for detailed documentation over each one of those.

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

### 7. 🏛️ Infrastructure

Here all the configurations needed to setup a new server to deploy the service are stored.
The tool that permits us to push the configurations automatically to each new service is called Ansible.

This module is intended to be used by system administrators and system administrators only, normal users or feature developers can ignore it without any kind of problem.