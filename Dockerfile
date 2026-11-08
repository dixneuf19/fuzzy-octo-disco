FROM python:3.14-slim@sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f AS builder

COPY --from=ghcr.io/astral-sh/uv:0.13@sha256:96f40d3904aad8d0bd010539001d36c8e2188b981e1334471a90c4a1d93bb490 /uv /uvx /bin/

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential cmake libopenblas-dev liblapack-dev \
  && rm -rf /var/lib/apt/lists/*

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_CACHE=1
ENV UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Keep in sync with pyproject.toml so uv sync reuses this build
ARG DLIB_VERSION=20.0.1
RUN uv venv /app/.venv && uv pip install --python /app/.venv dlib==${DLIB_VERSION}

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

FROM python:3.14-slim@sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f

RUN apt-get update \
  && apt-get install -y --no-install-recommends libopenblas0 \
  && rm -rf /var/lib/apt/lists/* \
  && useradd --system --uid 1000 app

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY fuzzyoctodisco/ fuzzyoctodisco/

USER app

EXPOSE 80

CMD ["uvicorn", "fuzzyoctodisco.main:app", "--host", "0.0.0.0", "--port", "80"]
