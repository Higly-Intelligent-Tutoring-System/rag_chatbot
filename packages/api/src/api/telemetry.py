from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor
from .config import ApiSettings

def init_telemetry(settings: ApiSettings):
    tracer_provider = register(
        #endpoint=settings.PHOENIX_COLLECTOR_ENDPOINT,
        project_name=settings.PHOENIX_PROJECT_NAME,
        auto_instrument=True,    # Auto-instrument based on installed OI dependencies
    )