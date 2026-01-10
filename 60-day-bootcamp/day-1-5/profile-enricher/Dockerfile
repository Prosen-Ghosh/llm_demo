# syntax=docker/dockerfile:1

# Builder stage: Build wheels for faster installation
FROM python:3.12-slim AS builder
WORKDIR /wheels
# Install build dependencies, create wheels, then remove build deps
RUN apt-get update && \
    apt-get install -y build-essential --no-install-recommends && \
    pip install --upgrade pip && \
    pip wheel --wheel-dir /wheels -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

# Final stage: Create the production image
FROM python:3.12-slim
WORKDIR /app

# Create a non-root user and group
RUN groupadd --system appuser && useradd --system --ingroup appuser appuser

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y ca-certificates --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copy wheels and requirements from the builder stage
COPY --from=builder /wheels /wheels
COPY requirements.txt .

# Install Python dependencies without caching
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

# Copy the application code
COPY . /app

# Set ownership of the app directory
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Set unbuffered output for Python
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
