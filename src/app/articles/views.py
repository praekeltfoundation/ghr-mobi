'''
Created on 21 Oct 2013

@author: michael
'''
from django.views import generic as generic_views

from tunobase.core import utils as core_utils

from app.articles import models

class Articles(generic_views.ListView):
    
    def get_queryset(self):
        return models.Article.objects.permitted()
    
class ArticleDetail(generic_views.DetailView):
    
    def get_object(self):
        return core_utils.get_permitted_object_or_404(
            models.Article, 
            slug=self.kwargs['slug']
        )