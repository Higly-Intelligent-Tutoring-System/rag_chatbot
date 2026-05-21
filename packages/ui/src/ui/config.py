from pydantic_settings import BaseSettings, SettingsConfigDict

class UiSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="UI_",
        extra="ignore",
    )

    API_DOMAIN: str
    API_PORT: int

    def api_url(self) -> str:
        return f"http://{self.API_DOMAIN}:{self.API_PORT}"
    
ui_settings = UiSettings()