'''
Created on 21 Oct 2013

@author: michael
'''
from django.views import generic as generic_views

from tunobase.core import (
    utils as core_utils,
    mixins as core_mixins
)

from app.newsfeed import models


class Newsfeed(core_mixins.GroupRequiredMixin, generic_views.ListView):
    groups_required = ['Ambassadors', 'Ni Nyampinga Journalists']

    def get_queryset(self):
        return models.FeedItem.objects.permitted()


class NewsfeedDetail(core_mixins.GroupRequiredMixin, generic_views.DetailView):
    groups_required = ['Ambassadors', 'Ni Nyampinga Journalists']

    def get_object(self):
        return core_utils.get_permitted_object_or_404(
            models.FeedItem,
            slug=self.kwargs['slug']
        )
