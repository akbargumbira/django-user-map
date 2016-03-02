# coding=utf-8
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

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.gis',
    'django.contrib.sites',
    'user_map',
    'leaflet',
    'bootstrapform',
    'rest_framework',
    'rest_framework_gis',
)

ROOT_URLCONF = 'user_map.tests.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware'
)

STATIC_ROOT = local_path('static/')
STATIC_URL = '/static/'

SECRET_KEY = 'django-user-map'

USER_MAP = {
    'project_name': 'Test Project',
    'favicon_file': '',
    'login_view': 'django.contrib.auth.views.login',
    'marker': {
        'icon': 'user_map/img/user-icon.png',
        'shadow': 'user_map/img/shadow-icon.png',  # or 'shadow': None
    },
    'leaflet_config': {
        'TILES': [
            (
                'OpenStreetMap',  # The title
                'http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
                # The tile URL
                ('© <a href="http://www.openstreetmap.org" '
                 'target="_parent">OpenStreetMap</a> and contributors, under '
                 'an <a href="http://www.openstreetmap.org/copyright" '
                 'target="_parent">open license</a>')  # The attribution
            )]
    },
    'roles': [
        {
            'id': 1,
            'name': 'User',
            'badge': 'user_map/img/inasafe-badge-user.png'
        },
        {
            'id': 2,
            'name': 'Trainer',
            'badge': 'user_map/img/inasafe-badge-trainer.png'
        },
        {
            'id': 3,
            'name': 'Developer',
            'badge': 'user_map/img/inasafe-badge-developer.png'
        }
    ],
    'api_user_fields': [
        'username'
    ],

}
