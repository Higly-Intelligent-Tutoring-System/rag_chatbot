from pydantic_settings import BaseSettings, SettingsConfigDict
from core import CoreSettings

class DocumentLoaderSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DOC_",
        extra="ignore",
    )

    CHUNK_SIZE: int
    CHUNK_OVERLAP: int
    MAX_PAGES_RECURSION: int
    URL_PATH: str
    PDF_PATH: str

document_loader_settings = DocumentLoaderSettings()
core_settings = CoreSettings()