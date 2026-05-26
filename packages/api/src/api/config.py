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
    RESPONSES_VS_ID: str

    AUTH_ENABLED: bool
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_SECONDS: int

    TELEMETRY_ENABLE: bool
    PHOENIX_COLLECTOR_DOMAIN: str
    PHOENIX_COLLECTOR_PORT: int
    PHOENIX_PROJECT_NAME: str

    SAVER_BACKEND: str
    STORER_BACKEND: str

    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_DOMAIN: str
    POSTGRES_PORT: str
    POSTGRES_SSL: str

    def postgres_db_uri(self, checkpointer=False) -> str:
        if checkpointer:
            return f"postgresql://{self.POSTGRES_USERNAME}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_DOMAIN}:{self.POSTGRES_PORT}/postgres?sslmode=disable"
        return f"postgresql+asyncpg://{self.POSTGRES_USERNAME}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_DOMAIN}:{self.POSTGRES_PORT}/postgres?sslmode=disable"
    
    def phoenix_collector_endpoint(self) -> str:
        return f"grpc://{self.PHOENIX_COLLECTOR_DOMAIN}:{self.PHOENIX_COLLECTOR_PORT}"

api_settings = ApiSettings()
core_settings = CoreSettings()