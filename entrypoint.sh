#!/bin/sh
set -e

echo "Waiting for Postgres (if needed)..."
# Optional: wait-for-it or simple sleep if DB not ready
# sleep 5

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting Gunicorn..."
exec gunicorn pairo_backend.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --timeout 120