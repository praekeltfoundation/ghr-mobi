from django.conf.urls import patterns, include, url

from app.core import views

urlpatterns = patterns('',
    url(r'^$',
        views.Index.as_view(
            template_name='core/index.html',
        ),
        name='index'
    ),
)