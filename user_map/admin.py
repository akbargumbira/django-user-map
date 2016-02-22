# coding=utf-8
"""Model Admin Class."""

from django.contrib.gis import admin

from leaflet.admin import LeafletGeoAdmin

from user_map.models import UserMap, Role


class UserMapAdmin(LeafletGeoAdmin):
    """Admin Class for User Map Model."""
    model = UserMap
    can_delete = False

admin.site.register(UserMap, UserMapAdmin)
admin.site.register(Role)
