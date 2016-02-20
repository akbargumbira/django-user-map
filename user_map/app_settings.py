# coding=utf-8
"""Configurations file for User Map.

..note: By design, you can override these settings from your project's
    settings.py with prefix 'USER_MAP' on the variable e.g
    'USER_MAP_USER_ICONS'.

    For mailing. as the default, it wil use 'DEFAULT_FROM_MAIL' setting from
    the project.
"""
from django.conf import settings


# USER_MODEL: The auth user model set in project's settings
USER_MODEL = settings.AUTH_USER_MODEL

# Leaflet Settings
LEAFLET_CONFIG = {
    'TILES': [
        (
            'OpenStreetMap', # The title
            'http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', # The tile URL
            ('© <a href="http://www.openstreetmap.org" '
             'target="_parent">OpenStreetMap</a> and contributors, under an '
             '<a href="http://www.openstreetmap.org/copyright" '
             'target="_parent">open license</a>') # The attribution
        )]
}
LEAFLET_TILES = LEAFLET_CONFIG['TILES'][0]

# USER MAP Settings
default_setting = {
    'project_name': 'InaSAFE',
    'brand_logo': '',
    'favicon_file': 'user_map/img/user-icon.png',
    'login_url': 'login',
    'marker': {
        'icon': 'user_map/img/user-icon.png',
        'shadow': 'user_map/img/shadow-icon.png'  # or 'shadow': None
    },
    'roles': [
        {
            'name': 'User',
            'badge': 'user_map/img/inasafe-badge-user'
        },
        {
            'name': 'Trainer',
            'badge': 'user_map/img/inasafe-badge-trainer'
        },
        {
            'name': 'Developer',
            'badge': 'user_map/img/inasafe-badge-developer'
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

# LOGO/BRAND
BRAND_LOGO = user_map_settings.get('brand_logo', default_setting['brand_logo'])

# FAVICON_FILE: Favicon for this apps
FAVICON_FILE = user_map_settings.get(
    'favicon_file', default_setting['favicon_file'])


# LOGIN_VIEW: The view to the login page
LOGIN_VIEW = user_map_settings.get(
    'login_url', default_setting['login_url'])

# MARKER
MARKER = user_map_settings.get(
    'marker', default_setting['marker'])

#  ROLES: All user roles and their badges
ROLES = user_map_settings.get('roles', default_setting['roles'])

#  API_USER_FIELDS
API_USER_FIELDS = user_map_settings.get(
    'api_user_fields', default_setting['api_user_fields'])
