# coding=utf-8
"""URI Routing configuration for this apps."""
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'user_map.views.index', name='index'),
    url(r'^users.json', 'user_map.views.get_users', name='get_users'),
    url(r'^register$', 'user_map.views.register', name='register'),
    url(r'^login$', 'user_map.views.login', name='login'),
    url(r'^logout$', 'user_map.views.logout', name='logout'),
    url(r'^update-profile$', 'user_map.views.update_user', name='update_user'),
)
