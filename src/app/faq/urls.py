'''
Created on 18 Oct 2013

@author: michael
'''
from django.conf.urls import patterns, url

from app.faq import views

urlpatterns = patterns(
    '',
    url(r'^$',
        views.FAQ.as_view(
            template_name='faq/faq.html',
        ),
        name='faq'),

    url(r'^(?P<slug>[-\w]+)/$',
        views.FAQDetail.as_view(
            template_name='faq/faq_detail.html'
        ),
        name='faq_detail'),
)
