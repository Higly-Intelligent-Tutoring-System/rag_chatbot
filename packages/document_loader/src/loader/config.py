from pydantic_settings import BaseSettings
from core import CoreSettings

class DocumentLoaderSettings(BaseSettings):
    CHUNK_SIZE: int
    CHUNK_OVERLAP: int
    MAX_PAGES_RECURSION: int
    URL_PATH: str
    PDF_PATH: str

    class Config:
        env_prefix = "DOC_"
        extra = "ignore"

document_loader_settings = DocumentLoaderSettings()
core_settings = CoreSettings()