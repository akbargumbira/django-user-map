# coding=utf-8
"""Configurations file for User Map.

..note: By design, you can override these settings from your project's
settings.py with prefix 'user_map' e.g
"""
from django.conf import settings

#  USER ICONS: All icon paths that are used.
default_user_icons = dict(
    user='user_map/img/user-icon.png',
    trainer='user_map/img/trainer-icon.png',
    developer='user_map/img/developer-icon.png',
    shadow='user_map/img/shadow-icon.png'
)
USER_ICONS = getattr(settings, 'USER_MAP_USER_ICONS', default_user_icons)
