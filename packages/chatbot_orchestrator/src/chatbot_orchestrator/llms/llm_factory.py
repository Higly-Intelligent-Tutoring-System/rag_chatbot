from typing import List
from langchain.chat_models import init_chat_model
from langchain_core.language_models.base import BaseLanguageModel
from langchain_openai import ChatOpenAI


class LLMFactory:
    @staticmethod
    def create(model_name: str, provider: str, temperature: float, 
               use_responses_api: bool = False, vector_store_ids: List[str] = None,
                 **kwargs) -> BaseLanguageModel:
        """Create LLM with optional graph-specific configurations"""
        
        if not use_responses_api:
            return init_chat_model(
                model=model_name,
                model_provider=provider,
                temperature=temperature
            )
        
        if provider == "openai" and use_responses_api:
            model = ChatOpenAI(
                model=model_name,
                use_responses_api=True,
                reasoning=kwargs.get("reasoning", {"effort": "low"}),
                output_version="v1"
            )
            vs_ids = vector_store_ids
            tools = [{
                "type": "file_search",
                "vector_store_ids": vs_ids if vs_ids else []
            },
            #{"type": "web_search"}
            ]
            return model.bind_tools(tools)
