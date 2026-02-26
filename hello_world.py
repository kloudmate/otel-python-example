import time
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

def setup_telemetry():
    """Configure OpenTelemetry Tracing."""
    
    # Basic resource attributes
    resource = Resource.create({
        "service.name": os.getenv("OTEL_SERVICE_NAME", "hello-world-simple"),
        "service.version": "1.0.0"
    })
    
    # Set up tracing provider
    provider = TracerProvider(resource=resource)
    
    # Check if we should export to OTLP or Console
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    
    if otlp_endpoint:
        otlp_endpoint = otlp_endpoint.strip()
        # Export to OTLP collector
        print(f"Configuring OTLP Exporter with endpoint: {otlp_endpoint}")
        headers_str = os.getenv("OTEL_EXPORTER_OTLP_HEADERS", "").strip()
        headers = {}
        if headers_str:
            for item in headers_str.split(","):
                if "=" in item:
                    key, val = item.split("=", 1)
                    headers[key] = val
                
        otlp_exporter = OTLPSpanExporter(
            endpoint=f"{otlp_endpoint}/v1/traces",
            headers=headers
        )
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    else:
        # Default to Console exporter for simple debugging
        print("No OTLP endpoint configured, using Console Exporter")
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    # Set the global default tracer provider
    trace.set_tracer_provider(provider)


def do_work(tracer):
    """Simulate some work with a nested span."""
    with tracer.start_as_current_span("nested_work_span") as child_span:
        child_span.set_attribute("work.detail", "simulating delay")
        child_span.add_event("Work started")
        time.sleep(0.5)
        child_span.add_event("Work completed")
        print("Finished simulated work.")


def main():
    setup_telemetry()
    
    # Get a tracer
    tracer = trace.get_tracer(__name__)
    
    print("Starting Hello World Application...")
    
    # Create the main span
    with tracer.start_as_current_span("hello_world_main_span") as span:
        span.set_attribute("application", "hello_world")
        span.set_attribute("message", "Hello, OpenTelemetry!")
        
        print("Hello, World!")
        
        # Call a function that creates a nested span
        do_work(tracer)
            
    print("Application completed.")
    
    # Ensure all spans are exported before exiting
    # The provider will be cleanly shut down when the script exits,
    # but explicitly calling shutdown guarantees everything is flushed.
    trace.get_tracer_provider().shutdown()


if __name__ == "__main__":
    main()
