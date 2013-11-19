'''
Created on 18 Oct 2013

@author: michael
'''
from django.conf.urls import patterns, url

from app.articles import views

urlpatterns = patterns('',
                       
    url(r'^$', 
        views.Articles.as_view(
            template_name='articles/articles.html',
            paginate_by=5,
        ),
        name='articles'
    ),
                       
    url(r'^(?P<slug>[-\w]+)/$', 
        views.ArticleDetail.as_view(
            template_name='articles/article_detail.html',
        ),
        name='article_detail'
    ),
)