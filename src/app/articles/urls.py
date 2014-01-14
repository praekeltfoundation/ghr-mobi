'''
Created on 18 Oct 2013

@author: michael
'''
from django.conf.urls import patterns, url

from app.articles import views

urlpatterns = patterns(
    '',
    url(r'^$',
        views.Articles.as_view(
        template_name='articles/articles.html',
        paginate_by=5), name='articles'),
    url(r'^(?P<slug>[-\w]+)/$',
        views.ArticleDetail.as_view(
            template_name='articles/article_detail.html',
            paginate_by=3
        ), name='article_detail'),
    url(r'^(?P<slug>[-\w]+)/all-comments/$',
        views.ArticleDetail.as_view(),
        name='article_all_comments'),
    url(r'^post-comment/(?P<slug>[-\w]+)/$',
        views.PostComment.as_view(),
        name='article_post_comment'),
)
