import requests

from base import create_app
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import opentelemetry.instrumentation.requests

from opentelemetry import trace
from opentelemetry.exporter import jaeger
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor, ConsoleSpanExporter

provider = TracerProvider()
trace.set_tracer_provider(provider)

jaeger_exporter = jaeger.JaegerSpanExporter(
    service_name='app_a',
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
trace.get_tracer_provider().add_span_processor(
    BatchExportSpanProcessor(ConsoleSpanExporter())
)

opentelemetry.instrumentation.requests.RequestsInstrumentor().instrument()
app = create_app('App A')
FastAPIInstrumentor.instrument_app(app)


tracer = trace.get_tracer('app_a')


@app.get("/")
def index_view():
    s = requests.Session()

    with tracer.start_as_current_span('get_welcome_message'):
        message = s.get("http://localhost:8001/welcome").json()
    return {"hello": message}
