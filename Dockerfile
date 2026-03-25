# use a slim Python image from docker
FROM python:3.12-slim-bookworm

# install uv from astral
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# set working directory
WORKDIR /app

# enable bytecode compilation and set environment variables
ENV UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1

# copy project configuration files first to leverage Docker cache
COPY pyproject.toml uv.lock ./

# install dependencies without installing the project itself
# this layer stays cached unless pyproject.toml or uv.lock change
RUN uv sync --frozen --no-install-project --no-dev

# copy rest of the application code
COPY . .

# FastAPI port
EXPOSE 8000

# create the directory for the SQLite DB if it doesn't exist
RUN mkdir -p src

# use uv to run the application
# use 'uv run' to ensure we use the synced virtual environment
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]