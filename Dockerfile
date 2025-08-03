# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies if needed (build tools, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY ./app ./app
COPY ./crawler ./crawler
COPY ./alembic ./alembic
COPY alembic.ini .

# Create data directory for SQLite persistence
RUN mkdir -p /app/data/raw_html

# Expose port that FastAPI runs on
EXPOSE 8000

# Start FastAPI server with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]