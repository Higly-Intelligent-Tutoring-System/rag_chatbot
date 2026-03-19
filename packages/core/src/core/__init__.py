from .embeddings import get_embeddings_model
from .vectordb import get_vector_store
from .config import CoreSettings

# __all__ defines what is exported when someone does "from core import *"
# It also serves as documentation for what is public API vs internal logic.
__all__ = [
    "get_embeddings_model",
    "get_vector_store",
    "CoreSettings"
]
