'''
Created on 21 Oct 2013

@author: michael
'''
from django.views import generic as generic_views

from tunobase.core import (
    utils as core_utils,
    views as core_views,
    mixins as core_mixins
)

from app.contacts import models


class ContactCategories(core_mixins.GroupRequiredMixin,
                        generic_views.ListView):
    groups_required = ['Ambassadors', 'Ni Nyampinga Journalists']

    def get_queryset(self):
        return models.ContactCategory.objects.permitted()


class ContactCategory(core_mixins.GroupRequiredMixin,
                      core_views.ListWithDetailView):
    groups_required = ['Ambassadors', 'Ni Nyampinga Journalists']

    def get_object(self):
        return core_utils.get_permitted_object_or_404(
            models.ContactCategory,
            slug=self.kwargs['slug']
        )

    def get_queryset(self):
        return self.object.contacts.permitted()
