'''
Created on 21 Oct 2013

@author: michael
'''
from django.views import generic as generic_views
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from tunobase.core import utils as core_utils

from app.root import views as root_views
from app.articles import models


class Articles(generic_views.ListView):

    def get_queryset(self):
        return models.Article.objects.permitted()


class ArticleDetail(root_views.CommentListDetail):

    def get_object(self):
        return core_utils.get_permitted_object_or_404(
            models.Article,
            slug=self.kwargs['slug']
        )


class PostComment(root_views.PostComment):

    def get_context_data(self, **kwargs):
        context = super(PostComment, self).get_context_data(**kwargs)
        obj = core_utils.get_permitted_object_or_404(
            models.Article,
            slug=self.kwargs['slug']
        )
        content_type_id = ContentType.objects.get_for_model(obj).id

        context.update({
            'content_type_id': content_type_id,
            'object': obj,
            'next': reverse('article_detail', kwargs=self.kwargs)
        })

        return context
