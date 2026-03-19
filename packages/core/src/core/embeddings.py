from langchain_huggingface import HuggingFaceEmbeddings
from .config import CoreSettings

def get_embeddings_model(settings: CoreSettings):
    """Returns the configured embedding model for the whole ecosystem."""
    # Centralized model definition
    return HuggingFaceEmbeddings(
        model_name=settings.EMBEDDING_MODEL_NAME,
        cache_folder=settings.CACHE_FOLDER
    )