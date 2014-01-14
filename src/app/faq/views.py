'''
Created on 21 Oct 2013

@author: michael
'''
from django.views import generic as generic_views

from tunobase.core import (
    utils as core_utils,
    mixins as core_mixins
)

from app.faq import models


class FAQ(core_mixins.GroupRequiredMixin, generic_views.ListView):
    groups_required = ['Ambassadors', 'Ni Nyampinga Journalists']

    def get_queryset(self):
        return models.FAQ.objects.permitted()


class FAQDetail(core_mixins.GroupRequiredMixin, generic_views.DetailView):
    groups_required = ['Ambassadors', 'Ni Nyampinga Journalists']

    def get_object(self):
        return core_utils.get_permitted_object_or_404(
            models.FAQ,
            slug=self.kwargs['slug']
        )
