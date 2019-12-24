from .default import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ.get('SECRET_KEY')

SECRET_KEY = 'ozfsu41n+x8$^_%_aqtug(fp1*5)=pz@w1+$h-_wfcjejp5-in'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    "167.71.122.121", 'rehsponse.com'
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rehsponsedb',
        'USER': 'db_admin',
        'PASSWORD': 'FiverrUser1!',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static-storage"),
]

# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')

