from .settings import *
import os
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = [
    '.onrender.com',
    'localhost',
    '127.0.0.1',
]

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CORS
CORS_ALLOWED_ORIGINS = [
    os.environ.get('FRONTEND_URL', 'http://localhost:5173'),
]

CSRF_TRUSTED_ORIGINS = [
    os.environ.get('FRONTEND_URL', 'http://localhost:5173'),
]

# Security settings for production
SECURE_SSL_REDIRECT = False  # Render handles SSL
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
