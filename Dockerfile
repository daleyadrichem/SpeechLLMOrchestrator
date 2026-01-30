FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the full project (uv sync needs everything)
COPY pyproject.toml README.md /app/
COPY src /app/src

# Install the package + API deps.
# If you created an `api` extra: use `.[api]`
RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir .

# Make src importable
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "speech_llm_orchestrator.api:app", "--host", "0.0.0.0", "--port", "8000"]