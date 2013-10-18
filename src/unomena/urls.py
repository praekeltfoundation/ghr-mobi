from django.conf.urls import patterns, include, url
from django.views import generic as generic_views
from django.views.generic import TemplateView
from django.conf import settings

from unomena import forms, views

urlpatterns = patterns('',
    (r'^auth/', include('unomena.auth.urls')),
)