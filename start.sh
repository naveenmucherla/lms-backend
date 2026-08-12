#!/usr/bin/env bash
set -e

echo "=== Running Database Migrations on Render Container ==="
python manage.py migrate --noinput

echo "=== Seeding Database Records (Quick Accounts & 15 Top Courses) ==="
python seed_data.py

echo "=== Starting Gunicorn WSGI Application ==="
exec gunicorn lms.wsgi:application
