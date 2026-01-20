# Base image
FROM python:3.12-slim

# Set env variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Collect static (safe even in dev)
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Start server
CMD ["gunicorn", "pairo_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
