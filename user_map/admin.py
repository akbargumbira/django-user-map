# coding=utf-8
"""Model Admin Class."""

from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin

from user_map.models import User, Role


class UserAdmin(LeafletGeoAdmin):
    """Admin Class for User Model."""
    list_display = ('name', 'email', 'role', 'website', 'email_updates',
                    'last_login')
    list_filter = ['role', 'is_approved', 'is_admin']
    search_fields = ['name', 'email']
    fieldsets = [
        ('Basic Information', {
            'fields': [
                'name', 'email', 'website', 'role', 'email_updates']}),
        ('Location', {'fields': ['location']}),
        ('Advanced Information', {
            'fields': ['is_approved', 'is_active', 'is_admin', 'last_login']}),
    ]


admin.site.register(User, UserAdmin)
admin.site.register(Role)
