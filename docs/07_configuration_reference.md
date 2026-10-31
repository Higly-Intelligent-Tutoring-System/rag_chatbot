# Creating the chatbot API `.env` files

The Docker Compose setup uses multiple service-specific environment files. Each service should have its own `.env` file, created from that service’s corresponding `*.env.dist` template. We can document the files one by one; this section covers the chatbot API. Its environment file must be named `.env`, not `api.env`.

From the envs/ directory, copy each template that you need with the following command:

```bash
cp .env.dist .env
```

For specific services, like *postgres*, you should add the name before `.env.dist` and at the start of the name of the new file.

Then edit `.env` and configure the values for your setup.

**PLEASE** keep secrets such as API keys, database passwords, and such in the local `.env` file, and do not commit that file to version control.

## API configuration

```dotenv
CORE_VECTOR_DB_BACKEND="chroma_local"
CORE_VECTOR_DB_DIR="./chroma_db_data"
CORE_VECTOR_DB_URL=
CORE_VECTOR_DB_API_KEY=
CORE_VECTOR_DB_COLLECTION="hits_documents"
CORE_EMBEDDING_MODEL_NAME="dbmdz/bert-base-italian-xxl-cased"
CORE_EMBEDDING_MODEL_PROVIDER="openai"
CORE_EMBEDDING_DIMENSIONS=1536
CORE_CACHE_FOLDER="./model_cache"

DOC_CHUNK_SIZE=1100
DOC_CHUNK_OVERLAP=100
DOC_BATCH_SIZE=32
DOC_MAX_PAGES_RECURSION=5
DOC_URL_PATH="data/urls.txt"
DOC_PDF_PATH="data/pdf_docs"
DOC_ALLOWED_FILE_EXTENSIONS='["pdf"]'

CHATBOT_GRAPH_NAME="NudgingItalian"
CHATBOT_MODEL_NAME="llama3.1:8b"
CHATBOT_PROVIDER_NAME="ollama"
CHATBOT_MODEL_TEMPERATURE=0.8

CHATBOT_USE_RESPONSES_API=False
CHATBOT_OPENAI_OUTPUT_VERSION=""
CHATBOT_OPENAI_RESPONSES_VS_ID=""
CHATBOT_OPENAI_REASONING_EFFORT=''

CHATBOT_SAVER_BACKEND="memory"
CHATBOT_STORER_BACKEND="memory"

CHATBOT_UNIVERSITY="University of Camerino UNICAM"

API_AUTH_ENABLED=False
API_SECRET_KEY=""
API_ACCESS_TOKEN_EXPIRE_SECONDS=36000
API_DOCS_ENABLED=False

API_TELEMETRY_ENABLE=False
API_PHOENIX_COLLECTOR_DOMAIN=http://localhost:6006/
API_PHOENIX_COLLECTOR_PORT=4317
API_PHOENIX_PROJECT_NAME="HITS-Chatbot"
OTEL_PYTHON_EXCLUDED_URLS="liveness"
OTEL_PYTHON_FASTAPI_EXCLUDED_URLS="liveness"

API_DATABASE_BACKEND="sqlite"
API_DATABASE_USERNAME=""
API_DATABASE_PASSWORD=""
API_DATABASE_DOMAIN="localhost"
API_DATABASE_PORT="5432"
API_DATABASE_DBNAME="hits"
API_DATABASE_SSL="disable"
API_SQLITE_PATH="./app.db"

PHOENIX_API_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GEMINI_API_KEY=
DEEPSEEK_API_KEY=
OTEL_EXPORTER_OTLP_INSECURE=true
```

### Parameter groups

- **Vector database and embeddings:** `CORE_VECTOR_DB_*`, `CORE_EMBEDDING_*`, and `CORE_CACHE_FOLDER` configure vector storage, the embedding model, and its cache.
- **Document processing:** `DOC_*` settings control document chunking, batch processing, recursive page loading, source paths, and allowed file extensions.
- **Chatbot and model:** `CHATBOT_GRAPH_NAME`, `CHATBOT_MODEL_NAME`, `CHATBOT_PROVIDER_NAME`, and `CHATBOT_MODEL_TEMPERATURE` configure the chatbot and its language model. The `CHATBOT_OPENAI_*` settings apply to the OpenAI Responses API configuration.
- **Conversation state:** `CHATBOT_SAVER_BACKEND` and `CHATBOT_STORER_BACKEND` select the backends used for saving and storing data.
- **University:** `CHATBOT_UNIVERSITY` identifies the institution associated with the chatbot.
- **API:** `API_*` settings configure authentication, API documentation, telemetry, and database access.
- **Credentials and telemetry export:** `*_API_KEY` settings hold provider credentials; `OTEL_EXPORTER_OTLP_INSECURE` configures the OpenTelemetry exporter.

### Values with special options

Confirm the valid options in the application configuration or code, then fill in the choices for these parameters:

- `CORE_VECTOR_DB_BACKEND`, the VectorDB engine for the retrieval.
    - `none` (usually used with OpenAI responses API)
    - `chroma_local` -> local implementation of ChromaDB with data saved in the repository.
    - `chroma_server` -> server implementation of ChromaDB (either self-hosted or on a remote host).
    - `supabase`
- `CORE_EMBEDDING_MODEL_NAME`
    - This depends on the prodiver, but generally you can find the correct name on its website.
- `CORE_EMBEDDING_MODEL_PROVIDER`
    - `huggingface`
    - `openai`
- `CHATBOT_GRAPH_NAME`
    - See the [chatbot architecture](./03_chatbot_architecture.md) file to discover all the possibilities. (If you suspect that the documentation is obsolete, all the graphs are registered [here](../packages/chatbot_orchestrator/src/chatbot_orchestrator/graphs/registry.py))
- `CHATBOT_MODEL_NAME`
    - This depends on the provider, but the same rules of `CORE_EMBEDDING_MODEL_NAME` apply.
    - When using *ollama* as the provider use the names returned by the command `ollama list`.
- `CHATBOT_PROVIDER_NAME`
    - Please, refer to the `model_provider` parameter in the official [langchain reference](https://reference.langchain.com/python/langchain/chat_models/base/init_chat_model), this will get injected inside.
- `CHATBOT_SAVER_BACKEND`
    - `memory`
- `CHATBOT_STORER_BACKEND`
    - `memory`
- `API_DATABASE_BACKEND`
    - `sqlite` -> suggested for local tests and initial developement.
    - `postgres` -> suggested for production environments.
- `API_DATABASE_SSL`
    - `enable`
    - `disable`
- `CHATBOT_USE_RESPONSES_API`, `API_AUTH_ENABLED`, `API_DOCS_ENABLED`, `API_TELEMETRY_ENABLE`, `OTEL_EXPORTER_OTLP_INSECURE` — boolean settings; document the accepted true/false format used by the application.

## UI configuration

```dotenv
UI_API_DOMAIN=
UI_API_PORT=
UI_API_AUTH=
UI_API_OVER_TLS=
```

Set `UI_API_AUTH` on `true` only when `API_AUTH_ENABLED` on the API env file has the same value.

## Other configurations

The other configurations are very straightforward and are not treated in this file.