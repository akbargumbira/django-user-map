# coding=utf-8
"""Configurations file for User Map.

..note: By design, you can override these settings from your project's
    settings.py with prefix 'USER_MAP' on the variable e.g
    'USER_MAP_USER_ICONS'.
"""
from django.conf import settings

# PROJECT_NAME: The project name for this apps e.g InaSAFE
default_project_name = 'InaSAFE'
PROJECT_NAME = getattr(settings, 'USER_MAP_PROJECT_NAME', default_project_name)

# FAVICON_FILE: Favicon for this apps
default_favicon_file = 'user_map/img/user-icon.png'
FAVICON_FILE = getattr(settings, 'USER_MAP_FAVICON_FILE', default_favicon_file)

#  USER ICONS: All icon paths that are used.
default_user_icons = dict(
    user='user_map/img/user-icon.png',
    trainer='user_map/img/trainer-icon.png',
    developer='user_map/img/developer-icon.png',
    shadow='user_map/img/shadow-icon.png'
)
USER_ICONS = getattr(settings, 'USER_MAP_USER_ICONS', default_user_icons)
