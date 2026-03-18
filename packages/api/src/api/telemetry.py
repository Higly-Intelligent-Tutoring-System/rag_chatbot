from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor

def init_telemetry():
    tracer_provider = register(
        # TODO: Insert in the configuration the endpoint (maybe even the project name to deliver smoothly to other universities)
        endpoint="http://localhost:4317",   # OTLP gRPC endpoint
        project_name="HITS-Chatbot",        # Default is 'default'
        auto_instrument=True                # Auto-instrument based on installed OI dependencies
    )