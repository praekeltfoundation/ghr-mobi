'''
Created on 21 Oct 2013

@author: michael
'''
from django.views import generic as generic_views
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from tunobase.core import utils as core_utils, mixins as core_mixins

from app.root import views as root_views
from app.discussions import models


class Discussions(generic_views.ListView):

    def get_queryset(self):
        return models.Discussion.objects.permitted()\
            .filter(for_ni_nyampinga_journalists_only=False)


class DiscussionDetail(root_views.CommentListDetail):

    def get_object(self):
        return core_utils.get_permitted_object_or_404(
            models.Discussion,
            slug=self.kwargs['slug'],
            for_ni_nyampinga_journalists_only=False
        )


class NiNyampingaDiscussions(core_mixins.GroupRequiredMixin,
                             generic_views.ListView):
    groups_required = ['Ambassadors', 'Ni Nyampinga Journalists']

    def get_queryset(self):
        return models.Discussion.objects.permitted()\
            .filter(for_ni_nyampinga_journalists_only=True)


class NiNyampingaDiscussionDetail(core_mixins.GroupRequiredMixin,
                                  root_views.CommentListDetail):
    groups_required = ['Ambassadors', 'Ni Nyampinga Journalists']

    def get_object(self):
        return core_utils.get_permitted_object_or_404(
            models.Discussion,
            slug=self.kwargs['slug'],
            for_ni_nyampinga_journalists_only=True
        )


class PostComment(root_views.PostComment):

    def get_context_data(self, **kwargs):
        context = super(PostComment, self).get_context_data(**kwargs)
        obj = core_utils.get_permitted_object_or_404(
            models.Discussion,
            slug=self.kwargs['slug']
        )
        content_type_id = ContentType.objects.get_for_model(obj).id

        context.update({
            'content_type_id': content_type_id,
            'object': obj,
            'next': reverse('discussion_detail', kwargs=self.kwargs)
        })

        return context
