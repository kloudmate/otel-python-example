"""
Simple Hello World Flask application with OpenTelemetry instrumentation.
This demonstrates both auto-instrumentation and custom spans.
"""
import time
from flask import Flask, jsonify
from opentelemetry import trace

# Get a tracer for creating custom spans
tracer = trace.get_tracer(__name__)

app = Flask(__name__)


@app.route('/')
def hello_world():
    """Simple hello world endpoint."""
    return jsonify({
        'message': 'Hello, World!',
        'status': 'success'
    })


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'otel-python-example'
    })


@app.route('/process')
def process():
    """
    Endpoint that demonstrates custom span creation.
    Simulates some processing work with custom spans.
    """
    with tracer.start_as_current_span("process_request") as span:
        # Add some attributes to the span
        span.set_attribute("request.type", "process")
        span.set_attribute("user.operation", "data_processing")
        
        # Simulate some work with nested spans
        result = do_work()
        
        span.set_attribute("result.count", result['processed_items'])
        
        return jsonify(result)


def do_work():
    """
    Worker function that demonstrates custom span creation.
    This simulates processing work with nested spans.
    """
    with tracer.start_as_current_span("do_work") as span:
        span.set_attribute("work.type", "data_processing")
        
        # Simulate step 1: Fetch data
        data = fetch_data()
        span.set_attribute("data.fetched", len(data))
        
        # Simulate step 2: Process data
        processed = process_data(data)
        span.set_attribute("data.processed", len(processed))
        
        return {
            'status': 'completed',
            'processed_items': len(processed),
            'original_items': len(data)
        }


def fetch_data():
    """
    Simulates fetching data with a custom span.
    """
    with tracer.start_as_current_span("fetch_data") as span:
        # Simulate database or API call
        time.sleep(0.1)
        data = ['item1', 'item2', 'item3', 'item4', 'item5']
        span.set_attribute("data.source", "simulated_database")
        span.set_attribute("data.count", len(data))
        return data


def process_data(data):
    """
    Simulates processing data with a custom span.
    """
    with tracer.start_as_current_span("process_data") as span:
        # Simulate some processing work
        time.sleep(0.15)
        processed = [item.upper() for item in data]
        span.set_attribute("processing.type", "uppercase_transformation")
        return processed


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
