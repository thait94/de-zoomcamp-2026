FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code

COPY pyproject.toml .python-version uv.lock ./
COPY ./data ./data

RUN uv sync --locked

COPY pipeline.py .

ENTRYPOINT ["uv", "run", "python", "pipeline.py"]