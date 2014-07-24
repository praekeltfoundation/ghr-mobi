'''
Created on 26 Mar 2013

@author: michael
'''
from copy import copy

from django import template
from django.core.exceptions import ImproperlyConfigured

try:
    from preferences import preferences
except ImportError:
    preferences = None

from tunobase.poll import forms, models
from app.experts import models as expert_model
register = template.Library()


@register.inclusion_tag('poll/inclusion_tags/poll_widget.html',
                        takes_context=True)
def poll_widget(context, pk=None, multiple_answers=False,
                randomize_answers=False):
    context = copy(context)
    expert_text = '' #------ Added by TechAff ----------#
    if pk is None:
        if preferences is None:
            raise ImproperlyConfigured(
                "No pk specified. Please add the preferences app to "
                "your settings.py file to load a default poll"
            )

        poll = preferences.SitePreferences.active_poll
        if poll is None:
            context.update({
                'error': True,
                'pk': pk
            })
            return context
        else:
            expert_text = expert_model.ExpertOpinion.objects.get(poll_id= poll.id).expert_opinion_text
    else:
        try:
            poll = models.PollQuestion.objects.permitted().get(pk=pk)
            ############ Added by Techaffinity #########
            try:
                expert_text = expert_model.ExpertOpinion.objects.get(poll_id= pk).expert_opinion_text
            except expert_model.ExpertOpinion.DoesNotExist:
                context.update({
                    'expert_text': '',
                    })
            ###############################################
        except models.PollQuestion.DoesNotExist:
            context.update({
                'error': True,
                'pk': pk
            })
            return context
    context.update({
        'form': forms.PollAnswerForm(
            poll=poll,
            multiple_answers=multiple_answers,
            randomize_answers=randomize_answers,
        ),
        'object_list': poll.answers.get_poll_percentages(),
        'expert_text': expert_text,
        'multiple_answers': multiple_answers
    })
    return context


@register.inclusion_tag('poll/inclusion_tags/poll_widget_research_tool.html',
                        takes_context=True)
def poll_widget_research_tool(context, pk=None, multiple_answers=False,
                randomize_answers=False):
    context = copy(context)
    try:
        polls = models.PollQuestion.objects.permitted().all()

    except models.PollQuestion.DoesNotExist:
        context.update({
            'error': True,
            'pk': pk
        })

    context.update({
        'polls' : polls
        })
    return context