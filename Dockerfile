# Dockerfile for theming.djust.org
# Builds djust-theming from source and runs the example_project Django app

FROM python:3.11-slim-bookworm

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install build tools
RUN pip install --no-cache-dir build

# Copy project files needed to build the wheel
COPY pyproject.toml README.md CHANGELOG.md ./
COPY djust_theming/ ./djust_theming/

# Build djust-theming wheel from source
RUN python -m build --wheel --outdir /tmp/wheels/

# Copy production requirements and optional pre-built wheels (e.g. djust from CI)
COPY example_project/requirements-prod.txt ./
COPY wheel[s]/ ./wheels/

# Install dependencies + local wheels
RUN pip install --no-cache-dir -r requirements-prod.txt \
    && if ls /wheels/*.whl 1>/dev/null 2>&1; then pip install --no-cache-dir /wheels/*.whl; fi \
    && pip install --no-cache-dir /tmp/wheels/djust_theming*.whl \
    && rm -rf /wheels /tmp/wheels

# Copy the theming showcase application
COPY example_project/ ./example_project/

WORKDIR /app/example_project

# Pre-collect static files during build
RUN DEBUG=False python manage.py collectstatic --noinput

# Copy entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Create necessary directories and non-root user
RUN mkdir -p /app/example_project/staticfiles \
    && useradd -m -u 1000 appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "example_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
