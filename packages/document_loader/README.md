# 📥 Document Loader

The **Document Loader** is a CLI tool designed to ingest data from various sources, split it into chunks, and upload embeddings to the configured Vector Database.

It relies on the `core` package for database connections and embedding models.

## ✨ Features

- **Web Crawler**: Recursively crawls websites (respecting domain boundaries).
- **PDF Loader**: Extracts text from PDF files.
- **Smart Chunking**: Uses strcture aware chunking from [Unstructured](https://unstructured.io/).
- **Abstracted Storage**: Uploads to ChromaDB or Supabase (depending on `core`).

## 🚀 Usage

Run the loader from the **root** of the monorepo using `uv`.

### Syntax

To analyze a single source use the following command:
```bash
(export $(cat envs/.env.dev | xargs) && uv run --package document_loader python -m loader.main [MODE] "[TARGET]")
```

**NOTE**: You need to [configure](../../docs/07_configuration_reference.md) the env file accordignly before executing the command. This stands for every command that needs to have an `export` before it.

## 📦 Batch Data Ingestion

The loader supports batch processing to ingest multiple resources in a single run.

### 1. Prepare your Data
Ensure your project root contains a `data` folder with the following structure:

```text
rag-monorepo/
├── data/
│   ├── urls.txt                    # List of URLs (one per line)
│   └── docs_for_ingestion/         # Folder containing .pdf files
```

Put in the file a url to parse recursively for each line and all the desired pdfs in the folder, then execute the following command:

```bash
(export $(cat envs/.env.dev | xargs) && uv run --package document_loader python -m loader.batch)
```

## 🏗️ Architecture

1. **Source**: Data is loaded via loader.sources.web or loader.sources.pdf.
2. **Transformation**: Text is split based on config.
3. **Embedding**: Text is converted to vectors using the shared model in core.
4. **Load**: Vectors are pushed to the database defined in VECTOR_DB_TYPE.

## 🛠️ Testing
Running Tests

We use requests-mock to test the crawler without making real HTTP requests.

```bash
# From monorepo root
uv run --package document-loader pytest
```

## Adding a New Source

To add support for a new format (e.g., Markdown):

1. Create `src/loader/sources/markdown.py`.
2. Implement a function that returns a list of Document objects.
3. Expose it in `src/loader/sources/__init__.py`.
4. Update `src/loader/main.py` to handle the new mode.

## Using OpenAI responses API VectorStores

Use this command to ingest for the OpenAI mode:

```bash
(export $(cat envs/.env.dev | xargs) && uv run --package document_loader python -m loader.packages/document_loader/src/loader/responses_autoingestion.py [--vs_id <id>])
```