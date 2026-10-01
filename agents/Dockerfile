FROM python:3.12-slim AS base
WORKDIR /app
ENV PYTHONPATH=/app
RUN pip install --no-cache-dir requests
CMD ["python", "agent.py"]

FROM base AS dev
RUN pip install --no-cache-dir \
    pytest pytest-cov ruff mypy types-requests

