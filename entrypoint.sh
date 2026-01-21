#!/bin/sh
<<<<<<< HEAD
set -e
=======
>>>>>>> 6c2b985e4a2a4ac77023812ff7487947185b2594

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn pairo_backend.wsgi:application --bind 0.0.0.0:8000
