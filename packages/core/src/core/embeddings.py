from langchain_huggingface import HuggingFaceEmbeddings
from core.config import EMBEDDING
import os

def get_embeddings_model():
    """Returns the configured embedding model for the whole ecosystem."""
    # Centralized model definition
    return HuggingFaceEmbeddings(model_name=EMBEDDING)