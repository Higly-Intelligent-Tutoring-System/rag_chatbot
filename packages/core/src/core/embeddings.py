from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from .config import CoreSettings

def get_embeddings_model(settings: CoreSettings):
    """Returns the configured embedding model for the whole ecosystem."""
    match settings.EMBEDDING_MODEL_PROVIDER.lower():
        case "huggingface":
            return HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL_NAME,
                cache_folder=settings.CACHE_FOLDER
            )
        case "openai":
            return OpenAIEmbeddings(
                model=settings.EMBEDDING_MODEL_NAME,
            )
        case _:
            raise ValueError(f"Unsupported embedding model provider: {settings.EMBEDDING_MODEL_PROVIDER}")