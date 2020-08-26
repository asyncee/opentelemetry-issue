import requests

from base import create_app
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import opentelemetry.instrumentation.requests

from opentelemetry import trace
from opentelemetry.exporter import jaeger
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

provider = TracerProvider()
trace.set_tracer_provider(provider)

jaeger_exporter = jaeger.JaegerSpanExporter(
    service_name='app_b',
    agent_host_name='localhost',
    agent_port=6831,
    collector_host_name='localhost',
    collector_port=14268,
    collector_endpoint='/api/traces?format=jaeger.thrift',
    collector_protocol='http',
)
trace.get_tracer_provider().add_span_processor(
    BatchExportSpanProcessor(jaeger_exporter)
)

opentelemetry.instrumentation.requests.RequestsInstrumentor().instrument()
app = create_app('App B')
FastAPIInstrumentor.instrument_app(app)


@app.get("/welcome")
def index_view():
    return "user"
