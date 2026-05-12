from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from core import CoreSettings

root = Path(__file__).resolve().parent  # src/evaluation
datasets_dir = root / "evals" / "datasets"

class EvalSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="API_",      # Takes the same wiring logic as API
        extra="ignore",
    )

    GRAPH_NAME: str
    MODEL_NAME: str
    PROVIDER_NAME: str
    MODEL_TEMPERATURE: float
    AUTH_ENABLE: bool
    TELEMETRY_ENABLE: bool

    PHOENIX_COLLECTOR_ENDPOINT: str
    PHOENIX_PROJECT_NAME: str

    SAVER_BACKEND: str
    STORER_BACKEND: str

    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_DOMAIN: str
    POSTGRES_PORT: str
    POSTGRES_SSL: str


eval_settings = EvalSettings()
core_settings = CoreSettings()