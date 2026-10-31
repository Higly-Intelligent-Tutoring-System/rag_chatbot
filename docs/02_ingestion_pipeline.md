# 📚 Ingestion Pipeline

A **knowledge base** is the collection of documents and other sources that gives the chatbot relevant information about its subject area. This guide explains how to prepare and ingest that content.

## 🗂️ Prepare the sources

Place the documents you want to include in:

```text
data/docs_for_ingestion/
```

Then choose one of the supported ingestion methods: use the project’s manual ingestion pipeline or an OpenAI-hosted vector store.

## 🧰 Option 1: Manual ingestion with a vector store

Use this option when the project’s loaders and batch-processing pipeline should handle ingestion.

- **Ingest a single source:** Use `main.py`. Pass `web` or `pdf` as the first parameter, followed by the URL or file path as the second parameter.
- **Ingest sources in bulk:** Use `batch.py` to process all websites listed in `urls.txt` and all documents in `data/docs_for_ingestion/`.
- **Loaders:** The web and PDF loaders are in the `document_loader` package, under `loaders/`. They use Unstructured to extract content.
- **Batch processing:** Each element follows the pipeline described in the [system architecture](01_system_architecture.md) documentation.

For the exact commands and launch instructions, see the module’s README.

## ☁️ Option 2: OpenAI-hosted vector store

Use this option to let OpenAI’s Responses API vector stores process and index the files. Launch this method with `responses_autoingestion.py`. Check the module’s [README](../packages/document_loader/README.md) for the exact command.

- **Create a new vector store:** Leave the `--vs_id` parameter blank. After creating the store, save its new ID in `CHATBOT_OPENAI_RESPONSES_VS_ID` in the configuration file. See the [configuration reference](07_configuration_reference.md).
- **Append to an existing vector store:** Provide its ID with the `--vs_id` parameter.

When files are added, OpenAI’s hosted service automatically chunks, embeds, and indexes them. Its API documentation describes the default chunking strategy as **800 tokens per chunk with 400 tokens of overlap**; a custom chunking strategy can also be specified. File processing is asynchronous, so ensure processing has finished before using the vector store. The public API documentation does not identify the specific embedding model used by the hosted service or expose every internal implementation detail.

Web ingestion is not implemented for this option. Use the web-search tool where web information is needed instead.