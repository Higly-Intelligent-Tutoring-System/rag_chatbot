from typing import Optional
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .llms.config import LLMConfig

class ChatbotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CHATBOT_",
        extra="ignore",
    )

    # Graph & LLM Selection
    GRAPH_NAME: str
    MODEL_NAME: str
    PROVIDER_NAME: str
    MODEL_TEMPERATURE: float
    
    # OpenAI Responses API (special case)
    USE_RESPONSES_API: bool = Field(default=False)
    OPENAI_RESPONSES_VS_ID: str = Field(default="")
    OPENAI_REASONING_EFFORT: str = Field(default="low")
    OPENAI_OUTPUT_VERSION: str = Field(default="v1")
    
    # Additional LLM parameters
    MODEL_MAX_TOKENS: Optional[int] = Field(default=None)
    MODEL_TOP_P: Optional[float] = Field(default=None)
    MODEL_FREQUENCY_PENALTY: Optional[float] = Field(default=None)

    # Short and long term memory configuration
    SAVER_BACKEND: str
    STORER_BACKEND: str

    @computed_field
    @property
    def llm_config(self) -> LLMConfig:
        """
        Build LLMConfig from environment settings.
        This is the source of truth for LLM instantiation.
        """
        return LLMConfig(
            model_name=self.MODEL_NAME,
            provider=self.PROVIDER_NAME,
            temperature=self.MODEL_TEMPERATURE,
            use_responses_api=self.USE_RESPONSES_API,
            vector_store_ids=[self.OPENAI_RESPONSES_VS_ID] if self.OPENAI_RESPONSES_VS_ID else [],
            reasoning={"effort": self.OPENAI_REASONING_EFFORT},
            output_version=self.OPENAI_OUTPUT_VERSION,
            max_tokens=self.MODEL_MAX_TOKENS,
            top_p=self.MODEL_TOP_P,
            frequency_penalty=self.MODEL_FREQUENCY_PENALTY,
        )