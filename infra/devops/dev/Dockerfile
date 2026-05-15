# ---- Stage 1: Builder ----
ARG BASE_IMAGE=python
ARG BASE_IMAGE_TAG=3.13-slim
FROM ${BASE_IMAGE}:${BASE_IMAGE_TAG} AS builder

ENV PYTHONUNBUFFERED=1

# Install build dependencies for Debian/slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        make \
        gcc \
        libc6-dev \
        python3-dev \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install and upgrade pip
RUN pip install --upgrade pip

# Install `uv` just for building dependencies
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install development dependencies (gunicorn + database + migration tools)
RUN uv pip install --no-cache-dir --system --group dev .

# Copy the app code and entrypoint script
COPY . .

# ---- Stage 2: Final Image ----
FROM ${BASE_IMAGE}:${BASE_IMAGE_TAG} AS final

# Only set essential environment variables
ENV PYTHONUNBUFFERED=1

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        bash \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /app /app

# Set permissions for entrypoint script (already copied via /app)
RUN chmod +x /app/infra/devops/scripts/entrypoint.sh

ENTRYPOINT ["/app/infra/devops/scripts/entrypoint.sh"]
