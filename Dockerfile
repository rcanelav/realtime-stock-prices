FROM python:3.13-slim AS base

COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter

WORKDIR /app

# Install build dependencies and clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir uv

# Dependency files
COPY pyproject.toml uv.lock .python-version ./

# Install dependencies using uv
RUN uv pip install --no-cache --system -e .

# App files
COPY ./src ./src

ENV PYTHONPATH=/app

ENV AWS_LWA_INVOKE_MODE=response_stream

EXPOSE 8080

CMD ["python", "src/main.py"]
