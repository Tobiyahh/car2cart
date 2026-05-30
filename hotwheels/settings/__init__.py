import os

# Default setting module for developer convenience.
# For production, set DJANGO_SETTINGS_MODULE=hotwheels.settings.production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotwheels.settings.local')

from .local import *
