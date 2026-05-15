# ---- Stage 1: Builder ----
ARG BASE_IMAGE=python
ARG BASE_IMAGE_TAG=3.13-alpine
FROM ${BASE_IMAGE}:${BASE_IMAGE_TAG} AS builder

ENV PYTHONUNBUFFERED=1

# Install build dependencies for Alpine
RUN apk add --no-cache \
    make \
    gcc \
    musl-dev \
    python3-dev \
    build-base

# Install and upgrade pip
RUN pip install --upgrade pip

# Install `uv` just for building dependencies
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install local development dependencies (everything except gunicorn)
RUN uv pip install --no-cache-dir --system --group local .

# Copy the app code and entrypoint script
COPY . .

# ---- Stage 2: Final Image ----
FROM ${BASE_IMAGE}:${BASE_IMAGE_TAG} AS final

# Only set essential environment variables
ENV PYTHONUNBUFFERED=1

# Install runtime dependencies
RUN apk add --no-cache bash curl

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /app /app

# Set permissions for entrypoint script (already copied via /app)
RUN chmod +x /app/infra/devops/scripts/entrypoint.sh

ENTRYPOINT ["/app/infra/devops/scripts/entrypoint.sh"]
