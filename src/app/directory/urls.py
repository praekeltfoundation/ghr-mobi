'''
Created on 18 Oct 2013

@author: michael
'''
from django.conf.urls import patterns, url

from app.directory import views

urlpatterns = patterns(
    '',
    url(r'^$',
        views.DirectoryCategories.as_view(
            template_name='directory/directory_categories.html',
        ),
        name='directory_categories'),

    url(r'^(?P<slug>[-\w]+)/$',
        views.DirectoryCategory.as_view(
            template_name='directory/directory_category.html'
        ),
        name='directory_category'),
)
