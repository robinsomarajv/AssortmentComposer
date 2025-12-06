# run_server.py

import os
# Import necessary OTel components
from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# --- 1. Set up the OTel Resource Name (Service Name) ---
# This value will be picked up by Langfuse
resource = Resource.create({
    "service.name": os.getenv("OTEL_RESOURCE_ATTRIBUTES", "assortment-planner-agent"),
})

# --- 2. Configure Trace Provider (for Spans/Traces) ---
trace_provider = TracerProvider(resource=resource)
# Configure exporter to send traces to the endpoint specified in env var OTEL_EXPORTER_OTLP_ENDPOINT
trace_exporter = OTLPSpanExporter()
processor = BatchSpanProcessor(trace_exporter)
trace_provider.add_span_processor(processor)
trace.set_tracer_provider(trace_provider)

# --- 3. Configure Metric Provider (less critical, but good practice) ---
metric_reader = PeriodicExportingMetricReader(OTLPMetricExporter())
metrics_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(metrics_provider)


# --- 4. Launch Uvicorn via programmatic interface ---

import uvicorn
import sys

# Ensure sys.argv is clean for uvicorn's parser
sys.argv = [
    "uvicorn",
    "main:agentic_assrtmnt",
    "--host", "0.0.0.0",
    "--port", "8080"
]

if __name__ == "__main__":
    # This starts your application with OTel already configured
    uvicorn.main()
