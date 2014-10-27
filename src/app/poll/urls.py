from django.conf.urls import patterns, url

from tunobase.poll import forms
from app.poll import views

urlpatterns = patterns('',

    url(r'^answer/(?P<pk>\d+)/$',
        views.PollAnswer.as_view(
            form_class=forms.PollAnswerForm,
            ajax_template_name='poll/includes/poll_results.html',
            template_name='poll/poll_results.html'
        ),
        name='poll_answer'),

    url(r'^results/(?P<pk>\d+)/$',
        views.PollResults.as_view(
            template_name='poll/poll_results.html'
        ),
        name='poll_results'),
)
