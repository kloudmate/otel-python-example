# OpenTelemetry Python Example

A simple Hello World Flask application demonstrating OpenTelemetry auto-instrumentation with custom spans.

## Features

- 🚀 Flask REST API with multiple endpoints
- 📊 OpenTelemetry auto-instrumentation for Flask
- 🎯 Custom spans for detailed tracing
- 🔧 Worker function demonstrating nested spans
- 🔐 Authorization header support via `OTEL_EXPORTER_OTLP_HEADERS`
- ⚙️ Configurable OTLP collector endpoint

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kloudmate/otel-python-example.git
cd otel-python-example
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

The application uses environment variables for OpenTelemetry configuration. Key variables:

- `OTEL_EXPORTER_OTLP_ENDPOINT`: The OTLP endpoint (default: `http://localhost:4318`)
- `OTEL_EXPORTER_OTLP_HEADERS`: Headers including Authorization (e.g., `Authorization=Bearer your-token`)
- `OTEL_SERVICE_NAME`: Service name for telemetry (default: `otel-python-example`)
- `OTEL_RESOURCE_ATTRIBUTES`: Additional resource attributes
- `OTEL_EXPORTER_OTLP_PROTOCOL`: Protocol to use (`http/protobuf` or `grpc`)

### Example Configuration

```bash
# .env file
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
OTEL_EXPORTER_OTLP_HEADERS=Authorization=Bearer your-token-here
OTEL_SERVICE_NAME=otel-python-example
OTEL_RESOURCE_ATTRIBUTES=deployment.environment=production,service.version=1.0.0
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
```

## Running the Application

### With Auto-Instrumentation (Recommended)

Use the provided script:
```bash
./run.sh
```

Or manually:
```bash
opentelemetry-instrument \
    --traces_exporter otlp \
    --metrics_exporter none \
    --logs_exporter none \
    python app.py
```

### Without Auto-Instrumentation

```bash
python app.py
```

Note: Without auto-instrumentation, you'll only see custom spans, not automatic Flask instrumentation.

## API Endpoints

### GET /
Simple hello world endpoint.

**Response:**
```json
{
  "message": "Hello, World!",
  "status": "success"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "otel-python-example"
}
```

### GET /process
Endpoint demonstrating custom spans and worker functionality.
Simulates data processing with nested spans.

**Response:**
```json
{
  "status": "completed",
  "processed_items": 5,
  "original_items": 5
}
```

## Custom Spans

The application demonstrates custom span creation in several ways:

1. **Request Processing Span** (`/process` endpoint):
   - Tracks the entire request processing
   - Adds attributes like request type and user operation

2. **Worker Span** (`do_work` function):
   - Demonstrates nested span creation
   - Tracks data fetching and processing steps

3. **Data Fetching Span** (`fetch_data` function):
   - Simulates database/API calls
   - Records data source and count

4. **Data Processing Span** (`process_data` function):
   - Simulates data transformation
   - Records processing type

## Testing

Test the endpoints using curl:

```bash
# Hello World
curl http://localhost:5000/

# Health Check
curl http://localhost:5000/health

# Process (with custom spans)
curl http://localhost:5000/process
```

## Viewing Traces

To view the traces, you need an OpenTelemetry collector and a backend like:
- Jaeger
- Zipkin
- Grafana Tempo
- Honeycomb
- Datadog
- New Relic

### Example: Using Jaeger

1. Run Jaeger all-in-one:
```bash
docker run -d --name jaeger \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 16686:16686 \
  -p 4318:4318 \
  jaegertracing/all-in-one:latest
```

2. Configure the application:
```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
export OTEL_SERVICE_NAME=otel-python-example
```

3. Run the application and make some requests

4. View traces at http://localhost:16686

## Docker Support

You can also run this application in Docker. Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["opentelemetry-instrument", "--traces_exporter", "otlp", "--metrics_exporter", "none", "--logs_exporter", "none", "python", "app.py"]
```

Build and run:
```bash
docker build -t otel-python-example .
docker run -p 5000:5000 \
  -e OTEL_EXPORTER_OTLP_ENDPOINT=http://host.docker.internal:4318 \
  -e OTEL_SERVICE_NAME=otel-python-example \
  -e OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token" \
  otel-python-example
```

## Architecture

```
┌─────────────────────┐
│   Flask App         │
│   (app.py)          │
│                     │
│  ┌──────────────┐   │
│  │ REST API     │   │
│  │ Endpoints    │   │
│  └──────────────┘   │
│                     │
│  ┌──────────────┐   │
│  │ Worker       │   │
│  │ Functions    │   │
│  └──────────────┘   │
└─────────────────────┘
         │
         │ OpenTelemetry
         │ Auto-Instrumentation
         │ + Custom Spans
         ▼
┌─────────────────────┐
│ OTLP Exporter       │
│ (with Auth Header)  │
└─────────────────────┘
         │
         ▼
┌─────────────────────┐
│ OTLP Collector      │
│ (Jaeger/Tempo/etc)  │
└─────────────────────┘
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
