from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from core.config import settings


def init_tracer():
    provider = TracerProvider(resource=Resource.create({"service.name": settings.project_name}))
    # Sets the global default tracer provider
    trace.set_tracer_provider(provider)

    jaeger_exporter = JaegerExporter(agent_host_name=settings.jaeger_host_name, agent_port=settings.jaeger_port)
    provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
