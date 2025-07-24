FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VENV_CREATE=false \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry and configure it to not create virtual environments
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Set work directory
WORKDIR /app

# Copy poetry files and README (needed for poetry install)
COPY pyproject.toml poetry.lock* README.md ./

# Install dependencies only (no project itself)
RUN poetry install --only=main --no-root && rm -rf $POETRY_CACHE_DIR

# Copy project files
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Install the project itself
RUN poetry install --only-root

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 8000

# Run the application (temporarily skip alembic migration to get basic app running)
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
