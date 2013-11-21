'''
Created on 21 Oct 2013

@author: michael
'''
from django.views import generic as generic_views

from tunobase.core import utils as core_utils, views as core_views

from app.directory import models

class DirectoryCategories(generic_views.ListView):
    
    def get_queryset(self):
        return models.DirectoryCategory.objects.permitted()
    
class DirectoryCategory(core_views.ListWithDetailView):
    
    def get_object(self):
        return core_utils.get_permitted_object_or_404(
            models.DirectoryCategory, 
            slug=self.kwargs['slug']
        )
    
    def get_queryset(self):
        return self.object.directory_items.permitted()