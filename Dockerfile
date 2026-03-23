FROM python:3.13-slim

WORKDIR /app

# Install the package with REST API support
COPY . .
RUN pip install --no-cache-dir ".[rest]"

# Database is stored in a volume-mountable directory
RUN mkdir -p /data
ENV OPENTIME_DB_PATH=/data/opentime.db
ENV OPENTIME_AGENT_ID=default
ENV OPENTIME_HOST=0.0.0.0
ENV OPENTIME_PORT=8080

EXPOSE 8080

# Health check against the /health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

CMD ["opentime-rest"]
