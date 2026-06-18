# Dockerfile for Glama MCP registry introspection (https://glama.ai/mcp/servers).
#
# Minimal image: install the official PyPI package and run the stdio MCP server.
# Glama uses this to build, start the container, and verify initialize + tools/list.
#
# No credentials required for introspection — env vars are only used when tools run.

FROM python:3.11-slim

WORKDIR /app

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    AOS_VALIDATOR_TARGET_DIR=/app

RUN pip install --no-cache-dir aos-compliance-validator-mcp==0.1.0

COPY examples/compliance_validator/mcp.json examples/manifest_annotation/manifest.json ./

RUN useradd --create-home --shell /bin/bash mcp \
    && chown -R mcp:mcp /app
USER mcp

ENTRYPOINT ["aos-compliance-validator"]
