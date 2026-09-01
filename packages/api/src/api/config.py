from dataclasses import Field
from typing import Optional

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from core import CoreSettings
from chatbot_orchestrator import ChatbotSettings

class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="API_",
        extra="ignore",
    )

    # Auth, Persistence, Telemetry, etc.
    AUTH_ENABLED: bool
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_SECONDS: int
    DOCS_ENABLED: bool

    TELEMETRY_ENABLE: bool
    PHOENIX_COLLECTOR_DOMAIN: str
    PHOENIX_COLLECTOR_PORT: int
    PHOENIX_PROJECT_NAME: str

    DATABASE_BACKEND: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_DOMAIN: str
    DATABASE_PORT: str
    DATABASE_DBNAME: str
    DATABASE_SSL: str
    SQLITE_PATH: str

    def get_db_uri(self) -> str:
        match self.DATABASE_BACKEND:
            case "sqlite":
                return f"sqlite+aiosqlite:///{self.SQLITE_PATH}"
            case "postgres":
                return f"postgresql+asyncpg://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_DOMAIN}:{self.DATABASE_PORT}/{self.DATABASE_DBNAME}"
            case _:
                raise ValueError(f"Unsupported database type: {self.DATABASE_BACKEND}")
            
    def phoenix_collector_endpoint(self) -> str:
        return f"grpc://{self.PHOENIX_COLLECTOR_DOMAIN}:{self.PHOENIX_COLLECTOR_PORT}"


api_settings = ApiSettings()
chatbot_settings = ChatbotSettings()
core_settings = CoreSettings()