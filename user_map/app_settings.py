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
    'project_name': 'InaSAFE',
    'favicon_file': 'user_map/img/user-icon.png',
    'login_view': 'django.contrib.auth.views.login',
    'marker': {
        'icon': 'user_map/img/user-icon.png',
        'shadow': 'user_map/img/shadow-icon.png'  # or 'shadow': None
    },
    'leaflet_config': {
        'TILES': [
            (
                'OpenStreetMap',  # The title
                'http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
                # The tile URL
                ('© <a href="http://www.openstreetmap.org" '
                 'target="_parent">OpenStreetMap</a> and contributors, '
                 'under an '
                 '<a href="http://www.openstreetmap.org/copyright" '
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
        'username', 'first_name', 'last_name'
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
