from .base import *


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = [
    '0.0.0.0',
    'localhost',
    'vbellofoods.herokuapp.com', # your herokuapp url
    '127.0.0.1'
]


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default':  dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dhzn9oqey',
    'API_KEY': '894294618768234',
    'API_SECRET': '8fqL8OfZKqSJChXcObtsRWqefPQ'
}

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True

db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)
DATABASES['default'].update(db_from_env)

