# 🤖 HITS Chatbot Monorepository

Welcome to the monorepository for the HITS Retrieval-Augmented Generation (RAG)
chatbot.

This repository contains multiple Python applications and shared packages managed as
a single workspace with [`uv`](https://docs.astral.sh/uv/). The workspace provides
consistent dependency management and versioning across the project.

## Documentation

- [Project overview](docs/00_overview.md)
- [System architecture](docs/01_system_architecture.md)
- [Chatbot architecture](docs/02_chatbot_architecture.md)
- [Ingestion pipeline](docs/03_ingestion_pipeline.md)
- [User manual](docs/04_user_manual.md)
- [Developer manual](docs/05_developer_manual.md)
- [Operations manual](docs/06_operations_manual.md)
- [Configuration reference](docs/07_configuration_reference.md)
- [Troubleshooting](docs/08_troubleshooting.md)
- [Security and privacy](docs/09_security_and_privacy.md)
- [Glossary](docs/10_glossary.md)

## Features

- Retrieval-Augmented Generation chatbot
- Shared Python packages
- Workspace-wide dependency management with `uv`
- Containerized development environment
- Support for local and remote language-model providers
- Document ingestion and processing
- Semantic search and retrieval

## ⚡ Prerequisites

The following tools are required for local development:

- Python 3.13 or later
- `uv`
- Podman and `podman compose`, or Docker and Docker Compose

For local development, Ollama is recommended as a language-model provider. It allows
developers to run a local model without consuming tokens from a paid remote provider.

### Installing `uv`

#### macOS and Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows PowerShell

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Additional requirements are documented in the
[developer manual](docs/05_developer_manual.md).

## 🚀 Setup and installation

### 1. Clone the repository

```bash
git clone https://github.com/<organization>/<repository>.git
cd <repository>
```

### 2. Create the local environment file

Create a local environment file from the provided template:

```bash
cp .env.dist .env
```

Review the generated `.env` file and provide the required values.

See the [configuration reference](docs/07_configuration_reference.md) for a
description of the available settings.

> **Important:** Do not commit `.env` or any file containing secrets.

### 3. Start the development environment

Using Podman:

```bash
podman compose -f docker-compose.dev.yml up
```

Using Docker:

```bash
docker compose -f docker-compose.dev.yml up
```

To stop the environment when using Podman:

```bash
podman compose -f docker-compose.dev.yml down
```

When using Docker, replace `podman` with `docker`:

```bash
docker compose -f docker-compose.dev.yml down
```

### 4. Verify the installation

Once the services are running, verify the system using the configured health-check
endpoint or application URL.

See the [operations manual](docs/06_operations_manual.md) for service URLs and
health-check procedures.

## Running without containers

The project can also be run directly from the host machine.

Synchronize all workspace packages and dependencies:

```bash
uv sync --all-packages
```

Instructions for starting individual services are available in the
[developer manual](docs/05_developer_manual.md).

## Repository structure

```text
rag-chatbot/
├── packages/
│   ├── core/                   # 🧠 Shared Library (Config, Database, Embeddings)
│   ├── document-loader/        # 📥 CLI Tool for Data Ingestion (Web & PDF)
│   ├── chatbot_orchestration/  # 🤖 Application layer (Chatbot engine)
│   ├── api/                    # ✉️ FastAPI Backend
│   ├── ui/                     # 🎓 Streamlit UI
│   ├── evaluation/             # 📐 RAGAS evaluation engine
│   └── infrastructure/         # 🏛️ Ansible configurations
│
├── pyproject.toml              # Workspace Definition
├── uv.lock                     # Unified Lockfile
├── .env.dist                   # Environment template
└── ...                         # Other Configuration and Documentation

The exact responsibilities of each package are described in the
[project overview](docs/00_overview.md).

## Environment types

The project may be used in the following environments:

- **Development:** Used for feature development and testing.
- **Staging:** Used for integration testing and final validation.
- **Production:** Used to run the final deployed system.

Environment-specific configuration and deployment procedures are documented in the
[operations manual](docs/06_operations_manual.md).

## Development commands

Install all workspace dependencies:

```bash
uv sync --all-packages
```

Run the test suite:

```bash
uv run pytest
```

Replace `<type-checker>` with the type-checking tool used by the project.

## Troubleshooting

If the project does not start correctly, consult the
[troubleshooting guide](docs/08_troubleshooting.md).

Common causes include:

- Missing environment variables
- An unavailable container engine
- A port conflict
- An unavailable language-model provider
- A missing Ollama model
- A service dependency that has not started
- Incorrect workspace configuration

## Contributing

Before submitting changes:

1. Install the project dependencies.
2. Run the test suite.
3. Run linting and formatting checks.
4. Run type checks, if configured.
5. Update the documentation when behavior or configuration changes.
6. Keep secrets and environment-specific configuration out of version control.

Detailed development instructions are available in the
[developer manual](docs/05_developer_manual.md).