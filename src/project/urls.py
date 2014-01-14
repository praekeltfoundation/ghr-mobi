from django.conf import settings
from django.conf.urls import patterns, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    (r'^', include('%s.urls' % settings.PROJECT_NAME)),

    (r'^commenting/', include('tunobase.commenting.urls')),
    (r'^tagging/', include('tunobase.tagging.urls')),
    (r'^poll/', include('tunobase.poll.urls')),
    (r'^tunosocial/', include('tunobase.social_media.tunosocial.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^secure/ckeditor/', include('ckeditor.urls')),
)

#------------------------------------------------------------------------------
# Django serves media
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root' : settings.MEDIA_ROOT,
          'show_indexes': True}
         ),
    )
