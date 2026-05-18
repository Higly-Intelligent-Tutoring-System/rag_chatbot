import io
from openai import OpenAI
from .config import core_settings, document_loader_settings

client = OpenAI()

def create_vector_store(name: str):
    vector_store = client.vector_stores.create(name=name)
    return vector_store

def ingest_raw_pdfs(folder_path: str, vs_id: str):
    from pathlib import Path
    pdf_files = list(Path(folder_path).glob("*.pdf"))
    file_streams = [open(f, "rb") for f in pdf_files]

    file_batch = client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vs_id,
        files=file_streams
    )
    print(file_batch.status)

    return file_batch

vector_store = client.vector_stores.create(name=core_settings.VECTOR_DB_COLLECTION)
print(f"Created vector store with ID: {vector_store.id}")
file_batch = ingest_raw_pdfs(document_loader_settings.PDF_PATH, vector_store.id)
print(f"File batch status: {file_batch.status}")
print(f"Ingestion completed for vector store ID: {vector_store.id}")