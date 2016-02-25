# coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^user-map/', include('user_map.urls', namespace='user_map')),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'admin/login.html'},
        name='my_login'),
    url(r'^admin/', include(admin.site.urls)),
)
