'''
Created on 18 Oct 2013

@author: michael
'''
from django.conf.urls import patterns, url

from tunobase.commenting import forms as commenting_forms

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
        ),
        name='discussion_detail'
    ),
                       
    url(r'^post-comment/(?P<slug>[-\w]+)/$', 
        views.PostComment.as_view(
            template_name='discussions/post_comment.html',
            form_class=commenting_forms.CommentForm
        ),
        name='discussion_post_comment'
    ),
)