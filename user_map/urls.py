# coding=utf-8
"""URI Routing configuration for this apps."""
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.conf import settings

import user_map.views

urlpatterns = [
    url(r'^$', user_map.views.IndexView.as_view(), name='index'),
    url(r'^add',
        login_required(
            user_map.views.UserAddView.as_view(),
            login_url=settings.USER_MAP['login_view']),
        name='add'),
    url(r'^update$',
        login_required(
            user_map.views.UserUpdateView.as_view(),
            login_url=settings.USER_MAP['login_view']),
        name='update'),
    url(r'^usermaps/$', user_map.views.UserMapList.as_view(),
        name='usermap-list'),
]
