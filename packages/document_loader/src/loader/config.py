from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from core import CoreSettings

class DocumentLoaderSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DOC_",
        extra="ignore",
    )

    @field_validator("ALLOWED_FILE_EXTENSIONS", mode="before")
    def _parse_extensions(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                # try JSON-like string
                import json
                return json.loads(v)
            return [s.strip() for s in v.split(",") if s.strip()]
        return v

    CHUNK_SIZE: int
    CHUNK_OVERLAP: int
    BATCH_SIZE : int
    MAX_PAGES_RECURSION: int
    URL_PATH: str
    PDF_PATH: str
    ALLOWED_FILE_EXTENSIONS: list[str]



document_loader_settings = DocumentLoaderSettings()
core_settings = CoreSettings()