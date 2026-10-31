## 🚀 Getting Started

### 1. Set up the repository

Clone the repository and move into its directory:

```bash
git clone https://github.com/Higly-Intelligent-Tutoring-System/rag_chatbot.git
cd rag-chatbot/
```

Sync the project’s Python environment with `uv`:

```bash
uv sync --all-packages
```

If it does not work out of the box, try to use the environment from the lockfile `uv.lock` via

```bash
uv sync --frozen
```

This installs the dependencies specified by the project. If `uv` is not installed, follow its installation instructions before running this command as specificed in the [README.md](../README.md)

Create the configuration files required by the services. Use the [Configuration Reference](./07_configuration_reference.md) to find the relevant templates, required values, and setup instructions. Keep secrets such as API keys in local configuration files; do not commit them to the repository.

**NOTE**: If you want to use ollama as your LLM provider, please remember to launch the `ollama serve` command in a terminal window.

### 2. Create the knowledge base

Prepare the chatbot’s knowledge base by following the steps in the [Ingestion Pipeline documentation](docs/03_ingestion_pipeline.md). Complete ingestion before starting the chatbot so the vector database contains the documents it needs to answer queries.

### 3. Start the development environment

From the repository root, start the development Docker Compose stack:

```bash
docker compose -f docker-compose.dev.yml up --build
```

The `--build` option builds or rebuilds the images before starting the services. To stop the stack, open another terminal and run:

```bash
docker compose -f docker-compose.dev.yml down
```

You can also press **Ctrl+C** in the initial shell and then use the down to make sure that each container has stopped.

Add the `-d` flag to the compose up command to run it as a background process, this allows the terminal to remain usable without stopping the containers.

When opening the chatbot, select **🌍 Generic** from the dropdown menu. Its label begins with the globe emoji showing Europe and Africa.