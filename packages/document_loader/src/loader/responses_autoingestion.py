import io
import re
import argparse
import sys
from pathlib import Path
from openai import OpenAI
from .config import core_settings, document_loader_settings

client = OpenAI()
vector_store = None

def create_vector_store(name: str):
    vector_store = client.vector_stores.create(name=name)
    return vector_store

def ingest_raw_files(folder_path: str, vs_id: str, extensions: list[str] = ["pdf"]):
    from pathlib import Path

    from pathlib import Path
    
    files = []
    for ext in extensions:
        files.extend(Path(folder_path).glob(f"*.{ext}"))
    
    if not files:
        print(f"No files found with extensions: {extensions}")
        return None
    
    file_streams = [open(f, "rb") for f in files]

    file_batch = client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vs_id,
        files=file_streams
    )
    print(file_batch.status)

    return file_batch

def main(vs_id: str | None = None):
    if vs_id:
        vector_store = client.vector_stores.retrieve(vs_id)
        print(f"Retrived vector store with ID: {vector_store.id}")
    else:
        vector_store = client.vector_stores.create(name=core_settings.VECTOR_DB_COLLECTION)
        print(f"Created vector store with ID: {vector_store.id}")

    file_batch = ingest_raw_files(document_loader_settings.PDF_PATH, vector_store.id, extensions=document_loader_settings.ALLOWED_FILE_EXTENSIONS)
    print(f"File batch status: {file_batch.status}")
    print(f"Ingestion completed for vector store ID: {vector_store.id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run evaluation queries in parallel")
    parser.add_argument(
        "--vs_id",
        type=str,
        required=False,
        help="Vector store id to ingest the new files (optional, if not given will create a new one)",
    )
    
    args = parser.parse_args()
    
    # Validate files exist
    pattern = r'^vs_[a-f0-9]{32}$'
    vs_id = args.vs_id
    if vs_id and not re.match(pattern, vs_id):
        print(f"❌ Error: The give vs_id does not respect the format: {args.vs_id}")
        sys.exit(1)

    main(vs_id)