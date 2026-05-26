import io
from openai import OpenAI
from .config import core_settings, document_loader_settings

client = OpenAI()

def create_vector_store(name: str):
    vector_store = client.vector_stores.create(name=name)
    return vector_store

def ingest_raw_files(folder_path: str, vs_id: str, extensions: list[str] = ["pdf"]):
    from pathlib import Path
    files = list(Path(folder_path).glob(f"*.{'|'.join(extensions)}"))
    file_streams = [open(f, "rb") for f in files]

    file_batch = client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vs_id,
        files=file_streams
    )
    print(file_batch.status)

    return file_batch



vector_store = client.vector_stores.create(name=core_settings.VECTOR_DB_COLLECTION)
print(f"Created vector store with ID: {vector_store.id}")
file_batch = ingest_raw_files(document_loader_settings.PDF_PATH, vector_store.id, extensions=document_loader_settings.ALLOWED_FILE_EXTENSIONS)
print(f"File batch status: {file_batch.status}")
print(f"Ingestion completed for vector store ID: {vector_store.id}")