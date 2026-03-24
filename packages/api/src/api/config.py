from pydantic_settings import BaseSettings, SettingsConfigDict
from core import CoreSettings

class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="API_",
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

    def postgres_db_uri(self):
        return f"postgresql://{self.POSTGRES_USERNAME}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_DOMAIN}:{self.POSTGRES_PORT}/postgres?sslmode={self.POSTGRES_SSL}"

api_settings = ApiSettings()
core_settings = CoreSettings()