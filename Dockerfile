FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Prevent Python buffering (important for logs in Jenkins)
ENV PYTHONUNBUFFERED=1

# Security: run as non-root user (production best practice)
RUN useradd -m appuser
USER appuser

EXPOSE 8000

# Healthcheck (VERY important for CI/CD pipelines)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl --fail http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
