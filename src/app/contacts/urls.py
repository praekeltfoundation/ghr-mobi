'''
Created on 18 Oct 2013

@author: michael
'''
from django.conf.urls import patterns, url

from app.contacts import views

urlpatterns = patterns('',
    url(r'^$', 
        views.ContactCategories.as_view(
            template_name='contacts/contact_categories.html',
        ),
        name='contact_categories'
    ),
                       
    url(r'^(?P<slug>[-\w]+)/$', 
        views.ContactCategory.as_view(
            template_name='contacts/contact_category.html'
        ),
        name='contact_category'
    ),
)