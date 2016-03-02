# coding=utf-8
"""Configurations file for User Map.

..note: By design, you can override these settings from your project's
    settings.py with prefix 'USER_MAP' on the variable e.g
    'USER_MAP_USER_ICONS'.
"""
from django.conf import settings


# USER_MODEL: The auth user model is set in project's settings
USER_MODEL = settings.AUTH_USER_MODEL

# USER MAP Settings
default_setting = {
    'project_name': 'Django User Map',
    'favicon_file': 'user_map/img/user-icon.png',
    'login_view': 'django.contrib.auth.views.login',
    'marker': {
        'icon': 'user_map/img/user-icon.png',
        'shadow': 'user_map/img/shadow-icon.png'  # or 'shadow': None
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
            'name': 'Django User',
            'badge': 'user_map/img/badge-user.png'
        },
        {
            'id': 2,
            'name': 'Django Trainer',
            'badge': 'user_map/img/badge-trainer.png'
        },
        {
            'id': 3,
            'name': 'Django Developer',
            'badge': 'user_map/img/badge-developer.png'
        }
    ],
    'api_user_fields': [
        # e.g 'username', 'first_name', 'last_name'
    ],
}

user_map_settings = getattr(settings, 'USER_MAP', default_setting)

# PROJECT_NAME: The project name for this apps e.g InaSAFE
PROJECT_NAME = user_map_settings.get(
    'project_name', default_setting['project_name'])

# FAVICON_FILE: Favicon for this apps
FAVICON_FILE = user_map_settings.get(
    'favicon_file', default_setting['favicon_file'])


# LOGIN_VIEW: The view to the login page
LOGIN_VIEW = user_map_settings.get(
    'login_view', default_setting['login_view'])

# MARKER
MARKER = user_map_settings.get(
    'marker', default_setting['marker'])

LEAFLET_CONFIG = user_map_settings.get(
    'leaflet_config', default_setting['leaflet_config'])
LEAFLET_TILES = LEAFLET_CONFIG['TILES']

#  ROLES: All user roles and their badges
ROLES = user_map_settings.get('roles', default_setting['roles'])

#  API_USER_FIELDS
API_USER_FIELDS = user_map_settings.get(
    'api_user_fields', default_setting['api_user_fields'])
