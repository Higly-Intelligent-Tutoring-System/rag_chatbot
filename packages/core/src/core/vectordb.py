from langchain_core.vectorstores import VectorStore
from langchain_chroma import Chroma
from langchain_community.vectorstores import SupabaseVectorStore
from supabase import create_client

from .config import CoreSettings
from .embeddings import get_embeddings_model

def get_vector_store(settings: CoreSettings) -> VectorStore:
    """
    Factory function to return the configured VectorStore.
    Controls VecDB implementation via environment variables.
    """
    db_backend = settings.VECTOR_DB_BACKEND.lower()
    embeddings = get_embeddings_model(settings)

    # Set the padding token
    if embeddings._client.tokenizer.pad_token is None:
        embeddings._client.tokenizer.pad_token = embeddings._client.tokenizer.eos_token

    print(f"✅ Embedding model loaded succsessfully!")

    match db_backend:
        case "supabase":
            url = settings.VECTOR_DB_URL
            key = settings.VECTOR_DB_API_KEY
            client = create_client(url, key)
            return SupabaseVectorStore(
                client=client, 
                embedding=embeddings, 
                table_name=settings.VECTOR_DB_COLLECTION
            )
        case "chroma_local":
            # Persist directory ensures data is saved to disk
            return Chroma(
                collection_name=settings.VECTOR_DB_COLLECTION,
                embedding_function=embeddings,
                persist_directory=settings.VECTOR_DB_DIR
            )
        case "chroma_server":
            return Chroma(
                collection_name=settings.VECTOR_DB_COLLECTION,
                embedding_function=embeddings,
                host=settings.VECTOR_DB_URL,
           )
        case _:
            raise ValueError(f"Unsupported VECTOR_db_backend: {db_backend}")
