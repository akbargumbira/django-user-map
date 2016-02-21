# coding=utf-8
"""URI Routing configuration for this apps."""
from django.conf.urls import url, patterns, include
from django.contrib.auth.decorators import login_required
from django.conf import settings

import user_map.views

urlpatterns = [
    url(r'^$', user_map.views.IndexView.as_view(), name='index'),
    url(r'^users/$', user_map.views.UserMapList.as_view(),
        name='usermap-list'),
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
    url(r'^download$', user_map.views.download, name='download'),
]

# expose static files and uploaded media if DEBUG is active
if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {
                'document_root': settings.MEDIA_ROOT,
                'show_indexes': True
            }),
        url(r'', include('django.contrib.staticfiles.urls'))
    )
