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
        'iconUrl': 'static/user_map/img/user-icon.png',
        'shadowUrl': 'static/user_map/img/shadow-icon.png',
        'iconSize': [19, 32],
        'shadowSize': [42, 35],
        'iconAnchor': [10, 0],
        'shadowAnchor': [12, 0],
    },
    'leaflet_config': {
        'TILES': [(
            # The title
            'MapQuest',
            # Tile's URL
            'http://otile{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png',
            # More valid leaflet option are passed here
            # See here: http://leafletjs.com/reference.html#tilelayer
            {
                'attribution':
                    '© <a href="http://www.openstreetmap.org" '
                    'target="_parent">OpenStreetMap'
                    '</a> and contributors, under an <a '
                    'href="http://www.openstreetmap.org/copyright" '
                    'target="_parent">open license</a>. Tiles Courtesy of '
                    '<a '
                    'href="http://www.mapquest.com/">MapQuest</a> <img '
                    'src="http://developer.mapquest.com/content/osm/mq_logo'
                    '.png"',
                'subdomains': '1234'

            }
        )]
    },
    'roles': [
        {
            'id': 1,
            'name': 'User',
            'badge': 'user_map/img/badge-user.png'
        },
        {
            'id': 2,
            'name': 'Trainer',
            'badge': 'user_map/img/badge-trainer.png'
        },
        {
            'id': 3,
            'name': 'Developer',
            'badge': 'user_map/img/badge-developer.png'
        }
    ],
    'api_user_fields': [
        'username'
    ],

}
