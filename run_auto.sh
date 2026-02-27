#!/bin/bash

# Script to run the Pure Auto-Instrumentation Demo Application

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | tr -d '\r' | xargs)
fi

echo "Starting Pure Auto-Instrumentation Demo (app_auto.py)..."
echo "This app uses no OpenTelemetry libraries in the code itself."

# Run the application with OpenTelemetry auto-instrumentation
opentelemetry-instrument \
    --traces_exporter otlp \
    --metrics_exporter none \
    --logs_exporter none \
    python app_auto.py
