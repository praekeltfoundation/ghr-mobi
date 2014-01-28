'''
Created on 21 Oct 2013

@author: michael
'''
from django.views import generic as generic_views

from preferences import preferences

from tunobase.core import utils as core_utils, mixins as core_mixins

from app.research_tool import models
    
class ResearchTool(core_mixins.GroupRequiredMixin, generic_views.DetailView):
    groups_required = ['Ambassadors', 'Ni Nyampinga Journalists']
    
    def get_object(self):
        return preferences.SitePreferences.research_tool
    
class ResearchToolDetail(core_mixins.GroupRequiredMixin, generic_views.DetailView):
    groups_required = ['Ambassadors', 'Ni Nyampinga Journalists']
    
    def get_object(self):
        return core_utils.get_permitted_object_or_404(
            models.ResearchTool, 
            slug=self.kwargs['slug']
        )