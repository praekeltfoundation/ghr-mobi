'''
Created on 18 Oct 2013

@author: michael
'''
from django.conf.urls import patterns, url

from app.discussions import views

urlpatterns = patterns('',
    # Update profile
    
    url(r'^$', 
        views.Discussions.as_view(
            template_name='discussions/discussions.html',
            paginate_by=5,
        ),
        name='discussions'
    ),
                       
    url(r'^(?P<slug>[-\w]+)/$', 
        views.DiscussionDetail.as_view(
            template_name='discussions/discussion_detail.html',
            paginate_by=3
        ),
        name='discussion_detail'
    ),
                       
    url(r'^ni-nyampinga/$', 
        views.NiNyampingaDiscussions.as_view(
            template_name='discussions/ni_nyampinga_discussions.html',
            paginate_by=5,
        ),
        name='ni_nyampinga_discussions'
    ),
                       
    url(r'^ni-nyampinga/(?P<slug>[-\w]+)/$', 
        views.NiNyampingaDiscussionDetail.as_view(
            template_name='discussions/ni_nyampinga_discussion_detail.html',
            paginate_by=3
        ),
        name='ni_nyampinga_discussion_detail'
    ),
                       
    url(r'^post-comment/(?P<slug>[-\w]+)/$', 
        views.PostComment.as_view(),
        name='discussion_post_comment'
    ),
)