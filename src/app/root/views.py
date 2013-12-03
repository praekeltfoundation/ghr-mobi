'''
Created on 21 Oct 2013

@author: michael
'''
from django.views import generic as generic_views
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from tunobase.core import views as core_views
from tunobase.commenting import forms as commenting_forms, models as commenting_models

from preferences import preferences

class Index(generic_views.TemplateView):
    
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        
        context['active_discussion'] = preferences.SitePreferences.active_discussion
        
        return context

class CommentListDetail(core_views.ListWithDetailView):
    template_name = 'root/all_comments.html'
        
    def get_queryset(self):
        content_type_id= ContentType.objects.get_for_model(self.object).id
        return commenting_models.CommentModel.objects.permitted().get_comments_for_object(
            content_type_id, 
            self.object.pk
        )

class PostComment(generic_views.FormView):
    form_class = commenting_forms.CommentForm
    template_name = 'root/post_comment.html'