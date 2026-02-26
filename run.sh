#!/bin/bash

# Script to run the Flask application with OpenTelemetry auto-instrumentation

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Run the application with OpenTelemetry auto-instrumentation
opentelemetry-instrument \
    --traces_exporter otlp \
    --metrics_exporter none \
    --logs_exporter none \
    python app.py
