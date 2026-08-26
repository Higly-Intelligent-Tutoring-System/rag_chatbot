from pydantic_settings import BaseSettings, SettingsConfigDict

class UiSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="UI_",
        extra="ignore",
    )

    API_DOMAIN: str
    API_PORT: int

    def api_url(self, university: str | None = None) -> str:
        """
        Generate API URL with optional university parameter.
        
        Args:
            university: University identifier (ita, slo, esp, rou, ltu)
        
        Returns:
            API URL string
        """
        base_url = f"http://{self.API_DOMAIN}:{self.API_PORT}"
        
        # If a specific university is provided, you can route to different subdomains/ports
        # This example assumes the backend routes based on path or query parameter
        if university:
            return f"{base_url}/api/{university}"  # or use query param: f"{base_url}?university={university}"
        
        return base_url
    
ui_settings = UiSettings()