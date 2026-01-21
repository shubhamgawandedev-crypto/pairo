FROM python:3.12-slim

# Prevent Python buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (you had libpq-dev for Postgres, gcc/pkg-config)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

# Make executable
RUN chmod +x entrypoint.sh

EXPOSE 8000

# Use shell form CMD (runs with /bin/sh -c) — safer for scripts
CMD ./entrypoint.sh