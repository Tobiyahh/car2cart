from .base import *

DEBUG = False

# In production, set the database connection via environment variables.
DATABASES['default'] = {
    'ENGINE': env('DATABASE_ENGINE', default='django.db.backends.postgresql'),
    'NAME': env('DATABASE_NAME', default='hotwheels'),
    'USER': env('DATABASE_USER', default='postgres'),
    'PASSWORD': env('DATABASE_PASSWORD', default='postgres'),
    'HOST': env('DATABASE_HOST', default='localhost'),
    'PORT': env('DATABASE_PORT', default='5432'),
}

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
