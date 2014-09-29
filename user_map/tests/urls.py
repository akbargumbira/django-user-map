from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^user-map/', include('user_map.urls', namespace='user_map'))
)
