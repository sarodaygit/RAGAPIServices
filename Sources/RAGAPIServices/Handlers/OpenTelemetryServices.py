 # OpenTelemetrySetup.py

from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from Utils.ConfigParserUtil import ConfigParserUtil

class OpenTelemetryServices:
    def __init__(self):
        self.config = ConfigParserUtil()

    def initialize_opentelemetry(self):
        service_name = self.config.getValue("OpenTelemetry", "service_name")
        jaeger_host = self.config.getValue("OpenTelemetry", "jaeger_host")
        jaeger_port = int(self.config.getValue("OpenTelemetry", "jaeger_port"))

        trace.set_tracer_provider(
            TracerProvider(
                resource=Resource.create({SERVICE_NAME: service_name})
            )
        )

        tracer_provider = trace.get_tracer_provider()
        jaeger_exporter = JaegerExporter(
            agent_host_name=jaeger_host,
            agent_port=jaeger_port,
        )   

        tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
