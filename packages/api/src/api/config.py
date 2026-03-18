from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Orchestrator
    graph_name: str = "BasicRagGraph"
    persistence_backend: str = "memory"

    # TODO: Add all of the necessary settings, such as:
        # - The model name and provider (not the API keys, it will be loaded thorugh env).
        # - The persistence_backend configurations (loaded here from env)
        # - The telemetry parameters to load from ENV.


settings = Settings()