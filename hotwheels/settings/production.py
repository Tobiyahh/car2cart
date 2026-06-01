from .base import *

DEBUG = False

# In production, set the database connection via environment variables.
DATABASES['default'] = env.db('DATABASE_URL', default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'))

# Configure WhiteNoise for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configure Cloudinary for media uploads
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
