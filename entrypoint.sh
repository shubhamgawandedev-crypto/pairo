#!/bin/sh
set -e  # Exit immediately if any command fails

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser only if all three required env vars are present
# and the user doesn't already exist
echo "Checking for superuser..."
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && \
   [ -n "$DJANGO_SUPERUSER_EMAIL" ] && \
   [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then

    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
username = "${DJANGO_SUPERUSER_USERNAME}"
email = "${DJANGO_SUPERUSER_EMAIL}"
password = "${DJANGO_SUPERUSER_PASSWORD}"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✅ Superuser created: $username")
else:
    print("ℹ️ Superuser '$username' already exists")
END

else
    echo "ℹ️ Skipping superuser creation (missing one or more env vars: DJANGO_SUPERUSER_USERNAME/EMAIL/PASSWORD)"
fi

echo "Starting Gunicorn..."
# Use $PORT (Render sets this automatically, usually 10000+)
# --workers 3 is reasonable for free tier
exec gunicorn pairo_backend.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 3 \
    --timeout 120 \
    --log-level info