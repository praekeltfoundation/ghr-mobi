'''
Created on 21 Oct 2013

@author: michael
'''
from django.views import generic as generic_views

from preferences import preferences

from tunobase.core import utils as core_utils, mixins as core_mixins
    
class ResearchTool(core_mixins.GroupRequiredMixin, generic_views.DetailView):
    groups_required = ['Ambassadors', 'Ni Nyampinga Journalists']
    
    def get_object(self):
        return preferences.SitePreferences.research_tool