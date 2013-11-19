'''
Created on 21 Oct 2013

@author: michael
'''
from django.views import generic as generic_views
from django.contrib.contenttypes.models import ContentType

from tunobase.core import utils as core_utils

from app.discussions import models

class Discussions(generic_views.ListView):
    
    def get_queryset(self):
        return models.Discussion.objects.permitted()
    
class DiscussionDetail(generic_views.DetailView):
    
    def get_object(self):
        return core_utils.get_permitted_object_or_404(
            models.Discussion, 
            slug=self.kwargs['slug']
        )
    
class PostComment(generic_views.FormView):
    
    def get_context_data(self, **kwargs):
        context = super(PostComment, self).get_context_data(**kwargs)
        obj = core_utils.get_permitted_object_or_404(
            models.Discussion, 
            slug=self.kwargs['slug']
        )
        content_type_id= ContentType.objects.get_for_model(obj).id
        
        context.update({
            'content_type_id': content_type_id,
            'object': obj,
        })
        
        return context
        