from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^auth/', include('app.auth.urls')),
    
    (r'^', include('app.root.urls')),
)