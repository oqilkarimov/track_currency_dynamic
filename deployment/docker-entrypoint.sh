#!/bin/sh

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Collect static files
echo "Collection static files"
python manage.py collectstatic --noinput

# Start server
echo "Starting server"
gunicorn config.wsgi --bind 0.0.0.0:8000
