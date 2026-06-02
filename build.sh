#!/usr/bin/env bash
# Render build script
set -o errexit

pip install -r requirements.txt

# Collect static files so WhiteNoise can serve them
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate

# Create superuser if needed
python deploy_setup.py
