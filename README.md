# 🤖 HITS Chatbot Monorepository

Welcome to the monolithic repository for the RAG (Retrieval-Augmented Generation) Chatbot of the HITS project. This repository manages multiple Python components and a shared core library using **uv** workspaces to ensure consistent dependencies and versioning.

## 🏗️ Architecture

The project is structured as a Monorepo with the following components:

```text
rag-monorepo/
├── packages/
│   ├── core/               # 🧠 Shared Library (Config, Database, Embeddings)
│   ├── document-loader/    # 📥 CLI Tool for Data Ingestion (Web & PDF)
│   └── rag-api/            # 🚧 FastAPI Backend (Chatbot Engine)
├── pyproject.toml          # Workspace Definition
├── uv.lock                 # Unified Lockfile
└── ...                     # Other Configuration and Documentation
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
    *Edit `.env` to define your Vector Database (Chroma/Supabase) and Embedding Model.*



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

*   **Usage**:
    ```bash
    # Crawl a website
    uv run --package document-loader python -m loader.main web "https://example.com"
    
    # Load a PDF
    uv run --package document-loader python -m loader.main pdf "./docs/manual.pdf"
    ```

### 3. 🚧 RAG API (`packages/rag-api`)
*Status: Under Construction*

This package will contain the FastAPI application serving the Chatbot REST endpoints.



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