import httpx
from opentelemetry import trace
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace import export

provider = trace_sdk.TracerProvider()
provider.add_span_processor(export.SimpleSpanProcessor(export.ConsoleSpanExporter()))
trace.set_tracer_provider(provider)

HTTPXClientInstrumentor().instrument()

# traces requests
with httpx.Client() as client:
    print(client.get("https://google.com?q=foo", follow_redirects=True))

# does not trace requests
# docker.for.mac.host.internal is used from inside devcontainer
# run HTTP proxy with docker run -p 3128:3128 ghcr.io/tarampampam/3proxy
with httpx.Client(proxy="http://docker.for.mac.host.internal:3128") as client:
    print(client.get("https://google.com?q=bar", follow_redirects=True))
