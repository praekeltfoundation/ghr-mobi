from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^auth/', include('unomena.auth.urls')),
)