# 🛡️ LRDEnE Guardian - Docker Image
# Copyright (c) 2026 LRDEnE. All rights reserved.

FROM python:3.11-slim

# Set metadata
LABEL maintainer="LRDEnE Technology Team <tech@lrden.com>"
LABEL description="LRDEnE Guardian - Advanced AI Safety & Hallucination Detection System"
LABEL version="1.0.0"
LABEL license="MIT"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LRDEN_GUARDIAN_VERSION="1.0.0" \
    LRDEN_GUARDIAN_HOME="/app"

# Create app directory
WORKDIR $LRDEN_GUARDIAN_HOME

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install LRDEnE Guardian
RUN pip install -e .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash lrden && \
    chown -R lrden:lrden $LRDEN_GUARDIAN_HOME
USER lrden

# Create directories for data and logs
RUN mkdir -p $LRDEN_GUARDIAN_HOME/data $LRDEN_GUARDIAN_HOME/logs

# Expose port for API (if implemented)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD lrden-guardian info || exit 1

# Default command
CMD ["lrden-guardian", "--help"]

# Build arguments
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

# Labels for build info
LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="LRDEnE Guardian" \
      org.label-schema.description="Advanced AI Safety & Hallucination Detection System" \
      org.label-schema.url="https://github.com/LRDEnE/lrden-guardian" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/LRDEnE/lrden-guardian.git" \
      org.label-schema.vendor="LRDEnE" \
      org.label-schema.version=$VERSION \
      org.label-schema.schema-version="1.0"
