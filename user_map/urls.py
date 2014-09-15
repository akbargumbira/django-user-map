# coding=utf-8
"""URI Routing configuration for this apps."""
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'user_map.views.index', name='index'),
    url(r'^users.json', 'user_map.views.get_users', name='get_users'),

    url(r'^register$', 'user_map.views.register', name='register'),
    url(r'^account-confirmation/(?P<uid>[0-9A-Za-z_\-]+)/(?P<key>.+)/$',
        'user_map.views.confirm_registration',
        name='confirm_registration'),

    url(r'^login$', 'user_map.views.login', name='login'),
    url(r'^logout$', 'user_map.views.logout', name='logout'),
    url(r'^update-profile$', 'user_map.views.update_user', name='update_user'),
    url(r'^delete-user$', 'user_map.views.delete_user', name='delete_user'),

    url(r'^password-reset/$', 'user_map.views.password_reset',
        name='password_reset'),
    url(r'^password-reset/done/$', 'user_map.views.password_reset_done',
        name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        'user_map.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^password-reset/complete/$',
        'user_map.views.password_reset_complete',
    name='password_reset_complete'),

    url(r'^download$', 'user_map.views.download', name='download'),
)
