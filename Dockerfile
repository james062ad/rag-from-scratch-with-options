# Use the official Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY pyproject.toml poetry.lock README.md ./
COPY src/ ./src/

# Install Poetry
RUN pip install --no-cache-dir poetry

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

# Expose port 8000
EXPOSE 8000

# Run FastAPI app with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
