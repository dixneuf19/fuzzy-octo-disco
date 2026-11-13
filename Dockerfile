FROM python:3.14-slim@sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f AS builder

COPY --from=ghcr.io/astral-sh/uv:0.13@sha256:5cc1805e2426484abca4ad46ea783bab281fdb225fd82d8ce6d66a81254bac85 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_CACHE=1
ENV UV_PYTHON_DOWNLOADS=never

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

FROM python:3.14-slim@sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f

RUN useradd --system --uid 1000 app

ENV PATH="/app/.venv/bin:$PATH"
ENV OPENCV_LOG_LEVEL=ERROR

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY fuzzyoctodisco/ fuzzyoctodisco/

USER app

EXPOSE 80

CMD ["uvicorn", "fuzzyoctodisco.main:app", "--host", "0.0.0.0", "--port", "80"]
