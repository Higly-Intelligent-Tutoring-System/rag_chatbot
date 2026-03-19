from pydantic_settings import BaseSettings

class CoreSettings(BaseSettings):
    VECTOR_DB_BACKEND: str = "chroma_local"
    VECTOR_DB_COLLECTION: str
    VECTOR_DB_API_KEY: str
    VECTOR_DB_URL: str
    VECTOR_DB_DIR: str
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    CACHE_FOLDER="./model_cache"

    class Config:
        env_prefix = "CORE_"
        extra = "ignore"