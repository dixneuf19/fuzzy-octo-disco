FROM python:3.15-slim@sha256:65a65fc7b30b06cb6df4930fd4650697cb23f4c2698ab81fc87e4b031bc36928 AS builder

COPY --from=ghcr.io/astral-sh/uv:0.13@sha256:96f40d3904aad8d0bd010539001d36c8e2188b981e1334471a90c4a1d93bb490 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_CACHE=1
ENV UV_PYTHON_DOWNLOADS=never

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

FROM python:3.15-slim@sha256:65a65fc7b30b06cb6df4930fd4650697cb23f4c2698ab81fc87e4b031bc36928

RUN useradd --system --uid 1000 app

ENV PATH="/app/.venv/bin:$PATH"
ENV OPENCV_LOG_LEVEL=ERROR

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY fuzzyoctodisco/ fuzzyoctodisco/

USER app

EXPOSE 80

CMD ["uvicorn", "fuzzyoctodisco.main:app", "--host", "0.0.0.0", "--port", "80"]
