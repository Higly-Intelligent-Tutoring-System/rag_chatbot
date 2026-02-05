from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
embedding_name = os.getenv("EMBEDDING")


def get_embeddings_model():
    """Returns the configured embedding model for the whole ecosystem."""
    # Centralized model definition
    return HuggingFaceEmbeddings(model_name=)
