import os
from typing import Optional
from langchain_core.vectorstores import VectorStore
from langchain_chroma import Chroma
from langchain_community.vectorstores import SupabaseVectorStore
from supabase import create_client

from core.config import VECTOR_DB_TYPE
from core.embeddings import get_embeddings_model

def get_vector_store(collection_name: str = "documents") -> VectorStore:
    """
    Factory function to return the configured VectorStore.
    Controls VecDB implementation via environment variables.
    """
    db_type = (VECTOR_DB_TYPE if VECTOR_DB_TYPE else "chroma_local").lower()
    embeddings = get_embeddings_model()

    print(f"✅ Embedding model loaded succsessfully!")

    match db_type:
        case "supabase":
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_SERVICE_KEY")
            client = create_client(url, key)
            return SupabaseVectorStore(
                client=client, 
                embedding=embeddings, 
                table_name=collection_name
            )
        case "chroma_local":
            # Persist directory ensures data is saved to disk
            persist_dir = os.getenv("CHROMA_DB_DIR", "./chroma_db_data")
            return Chroma(
                collection_name=collection_name,
                embedding_function=embeddings,
                persist_directory=persist_dir
            )
        case "chroma_server":
            return Chroma(
                collection_name="example_collection",
                embedding_function=embeddings,
                host=os.getenv("CHROMA_URL"),
           )
        case _:
            raise ValueError(f"Unsupported VECTOR_DB_TYPE: {db_type}")
