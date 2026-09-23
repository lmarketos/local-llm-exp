FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app

RUN pip install --no-cache-dir requests pytest pytest-cov

COPY agent.py .
COPY tests ./tests

CMD ["python", "agent.py"]

