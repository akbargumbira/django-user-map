import os
local_path = lambda path: os.path.join(os.path.dirname(__file__), path)

SITE_ID = 1

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'test_db',
        'HOST': 'localhost',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': ''
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.gis',
    'leaflet',
    'bootstrapform',
    'user_map',
]

ROOT_URLCONF = 'user_map.tests.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'user_map.context_processors.user_map_settings',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTH_USER_MODEL = 'user_map.User'
AUTHENTICATION_BACKENDS = [
    'user_map.auth_backend.UserMapAuthBackend',
    'django.contrib.auth.backends.ModelBackend']

STATIC_ROOT = local_path('static/')
STATIC_URL = '/static/'

SECRET_KEY = 'django-user-map'
