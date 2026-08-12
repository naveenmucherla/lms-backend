#!/usr/bin/env bash
# exit on error
set -o errexit

echo "=== Installing Dependencies ==="
pip install -r requirements.txt

echo "=== Running Migrations ==="
python manage.py migrate --noinput

echo "=== Seeding Quick Accounts & 15 Top Courses ==="
python seed_data.py

echo "=== Collecting Static Files ==="
python manage.py collectstatic --noinput
