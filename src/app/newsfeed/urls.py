'''
Created on 18 Oct 2013

@author: michael
'''
from django.conf.urls import patterns, url

from app.newsfeed import views

urlpatterns = patterns('',
    url(r'^$', 
        views.Newsfeed.as_view(
            template_name='newsfeed/newsfeed.html',
            paginate_by=5
        ),
        name='newsfeed'
    ),
                       
    url(r'^(?P<slug>[-\w]+)/$', 
        views.NewsfeedDetail.as_view(
            template_name='newsfeed/newsfeed_detail.html'
        ),
        name='newsfeed_detail'
    ),
)