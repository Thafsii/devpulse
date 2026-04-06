FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (layer-cached separately from source code)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source (env vars are injected at runtime, NOT baked in here)
COPY app/ ./app/

EXPOSE 8000

# Single worker is appropriate for Railway's single-container deployments.
# Use --workers 1 with --loop uvloop for best async performance.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
