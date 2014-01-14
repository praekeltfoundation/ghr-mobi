'''
Created on 18 Oct 2013

@author: michael
'''
from django.conf.urls import patterns, url

from app.galleries import views

urlpatterns = patterns(
    '',
    # Update profile

    url(r'^$',
        views.Galleries.as_view(
            template_name='galleries/galleries.html',
            paginate_by=5,
        ),
        name='galleries'),

    url(r'^(?P<slug>[-\w]+)/$',
        views.GalleryDetail.as_view(
            template_name='galleries/gallery_detail.html',
            paginate_by=3
        ),
        name='gallery_detail'),

    url(r'^image/(?P<pk>\d+)/$',
        views.GalleryImageDetail.as_view(
            template_name='galleries/gallery_image_detail.html',
            paginate_by=3
        ),
        name='gallery_image_detail'),

    url(r'^(?P<slug>[-\w]+)/all-comments/$',
        views.GalleryDetail.as_view(),
        name='gallery_all_comments'),

    url(r'^post-comment/(?P<slug>[-\w]+)/$',
        views.PostComment.as_view(),
        name='gallery_post_comment'),
)
