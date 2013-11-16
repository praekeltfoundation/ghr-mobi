from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^authentication/', include('app.authentication.urls')),
    
    (r'^', include('app.bulk_load_tester.urls')),
    (r'^', include('app.root.urls')),
)