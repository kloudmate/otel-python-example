#!/bin/bash

# Script to run the Manual Instrumentation + Custom Attributes Demo Application

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | tr -d '\r' | xargs)
fi

echo "Starting Manual + Custom Attributes Demo (app_manual.py)..."
echo "This app nests custom business spans and attributes into auto-instrumented flask routes."

# Run the application with OpenTelemetry auto-instrumentation
opentelemetry-instrument \
    --traces_exporter otlp \
    --metrics_exporter none \
    --logs_exporter none \
    python app_manual.py
