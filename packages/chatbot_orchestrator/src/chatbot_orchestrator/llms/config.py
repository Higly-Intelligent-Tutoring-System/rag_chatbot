from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class LLMConfig:
    """Configuration for LLM instantiation"""
    
    # Core LLM parameters
    model_name: str
    provider: str
    temperature: float
    
    # OpenAI Responses API specific
    use_responses_api: bool = False
    vector_store_ids: list = None
    reasoning: Dict[str, str] = None
    output_version: str = "v1"
    
    # Optional general parameters
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    
    def __post_init__(self):
        """Initialize defaults for mutable fields"""
        if self.vector_store_ids is None:
            self.vector_store_ids = []
        if self.reasoning is None:
            self.reasoning = {"effort": "low"}
    
    def to_factory_kwargs(self) -> Dict[str, Any]:
        """Convert dataclass to kwargs for LLMFactory.create()"""
        return asdict(self)
    
    def __repr__(self) -> str:
        """Pretty print for debugging"""
        return (
            f"LLMConfig(model={self.model_name}, provider={self.provider}, "
            f"temp={self.temperature}, responses_api={self.use_responses_api})"
        )
