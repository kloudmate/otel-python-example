# KloudMate OpenTelemetry Integration Guide (Python)

This repository provides a clear, step-by-step demonstration of how to integrate your Python (Flask) applications with the KloudMate observability platform.

We demonstrate two primary approaches:
1. **Zero-Code Auto-Instrumentation**: Instantly gain visibility into your HTTP routes, database calls, and external requests without writing a single line of OpenTelemetry code.
2. **Manual Instrumentation**: Enrich your auto-generated traces with deep, business-specific custom spans, attributes, and span events (demonstrated via an E-Commerce checkout scenario called _`K-Commerce`_).

---

## Prerequisites

- **Python**: 3.8 or higher.
- **KloudMate Account**: You will need your Workspace API Key to send telemetry data to your dashboard. (You can find this on your KloudMate dashboard under Settings -> Workspaces -> Click on **API Keys** on your desired Workspace)

---

## Installation & Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure KloudMate Telemetry Exporter:**
   Copy the example environment file and add your KloudMate API Key.
   ```bash
   cp .env.example .env
   ```
   Open `.env` and configure your API key and service name you want:
   ```env
   # .env file
   OTEL_EXPORTER_OTLP_ENDPOINT=https://otel.kloudmate.com:4318
   OTEL_EXPORTER_OTLP_HEADERS=Authorization=YOUR_KLOUDMATE_API_KEY
   OTEL_SERVICE_NAME=otel-python-example
   ```

---

## Approach 1: Zero-Code Auto-Instrumentation

The fastest way to get started with KloudMate. By running your existing application through the `opentelemetry-instrument` wrapper, OpenTelemetry automatically injects itself into standard Python libraries (like Flask, Requests, SQLAlchemy, etc.) and generates traces.

**Target File**: `app_auto.py` (Notice this file imports *no* OpenTelemetry libraries).

### Running the Demo
Start the auto-instrumented application:
```bash
./run_auto.sh
```

### Try these endpoints:
- `curl http://localhost:5000/api/users`: Simulates a standard database delay. Auto-instrumentation will capture the exact duration of the request automatically.
- `curl http://localhost:5000/api/computation`: Simulates heavy CPU load.

*Outcome*: Check your KloudMate dashboard to see beautiful traces tracking the entry and exit of your HTTP requests instantly.

---

## Approach 2: Manual Instrumentation (Advanced)

While auto-instrumentation is powerful, distributed architectures often require deeper insights into custom business logic. `app_manual.py` demonstrates how to layer manual tracing over auto-instrumentation.

**Target File**: `app_manual.py`

### The K-Commerce Simulation
The `/checkout` endpoint in this application simulates a complex K-Commerce checkout pipeline:
- `inventory.check`: A custom span tracking inventory, which may throw a simulated "Out of Stock" exception.
- `payment.process`: Adds rich custom attributes (`payment.amount`, `payment.gateway`) and milestones via **Span Events** (`payment.gateway.initiated`).
- `logistics.schedule`: Generates a mock tracking number appended to the trace.

By leveraging `span.set_attribute()`, `span.add_event()`, and `span.record_exception()`, you gain immense filtering textuality inside the KloudMate dashboard.

### Running the Demo
Start the manually instrumented application:
```bash
./run_manual.sh
```

### Try the Checkout Pipeline:
Trigger the stochastic K-Commerce scenario (which has built-in simulated failure rates to demonstrate OpenTelemetry error reporting):
```bash
curl http://localhost:5000/checkout
```

*Outcome*: In KloudMate, you will see a detailed, nested trace starting from the HTTP POST route, delving down into specific operations like `inventory.check` and `payment.process`, complete with their associated metadata and internal event timelines.

---

## Viewing Your Data in KloudMate

1. Log in to your [KloudMate Dashboard](https://app.kloudmate.com).
2. Navigate to the **APM / Services** Module section.
3. Select the service name `otel-python-example` (or whatever you set `OTEL_SERVICE_NAME` to in your `.env` file).
4. Alternatively you can view individual traces emitted by your application, by clicking on **Traces** Module.
5. Click into individual traces to view request latency, custom attributes (e.g., `user.id`, `payment.gateway`), and application errors directly mapped to the source code exceptions.

---

<div align="center">

**Made with 🧡 by the KloudMate Team**

[Website](https://kloudmate.com) • [KloudMate Agents](https://github.com/kloudmate/km-agent) • [Support](mailto:support@kloudmate.com)

</div>
