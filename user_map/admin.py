    # coding=utf-8
"""Model Admin Class."""

from django.contrib.gis import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from leaflet.admin import LeafletGeoAdmin

from user_map.models import UserMap, Role


class UserMapAdmin(LeafletGeoAdmin):
    """Admin Class for User Map Model."""
    model = UserMap
    can_delete = False
    # list_display = ('name', 'email', 'role', 'website', 'email_updates',
    #                 'last_login', 'is_confirmed', 'is_admin')
    # list_filter = ['role', 'is_confirmed', 'is_admin']
    # search_fields = ['name', 'email']
    # fieldsets = [
    #     ('Basic Information', {
    #         'fields': [
    #             'name', 'email', 'website', 'role', 'email_updates']}),
    #     ('Location', {'fields': ['location']}),
    #     ('Advanced Information', {
    #         'fields': ['is_confirmed', 'is_active', 'is_admin', 'last_login']
    #     }),
    # ]

from django.contrib.auth.models import User

# class UserAdmin(BaseUserAdmin):
#     """Define the new User Admin plugging the UserMap."""
#     inlines = (UserMapAdmin, )

# Re-register User Admin
# admin.site.unregister(get_user_model())
admin.site.register(UserMap, UserMapAdmin)
admin.site.register(Role)
