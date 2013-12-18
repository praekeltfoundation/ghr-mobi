'''
Created on 18 Dec 2013

@author: michael
'''
from datetime import datetime

from dateutil.relativedelta import relativedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from photon import Client

from tunobase.commenting import models as comment_models
from tunobase.social_media.tunosocial import models as tunosocial_models

from preferences import preferences

client = Client(
    server="http://localhost:8000/",
)


def _push_total_week_month(api_key, total_val, week_val,
                           month_val, change_val):
    client.send(
       samples=(
           ("% Change", change_val),
           ("Past Month", month_val),
           ("Past Week", week_val),
           ("Total", total_val),
       ),
       api_key=api_key,
       timestamp=datetime.now(),
    )


def _push_top_5_articles(api_key, article_list):
    client.send(
       samples=article_list,
       api_key=api_key,
       timestamp=datetime.now(),
    )


def _push_total(api_key, queryset, date_field):
    week_kwargs = {
       '%s__gte' % date_field: timezone.now() + relativedelta(weeks=-1)
    }
    month_kwargs = {
       '%s__gte' % date_field: timezone.now() + relativedelta(months=-1)
    }
    previous_kwargs = {
       '%s__gte' % date_field: timezone.now() + relativedelta(months=-2),
       '%s__lt' % date_field: timezone.now() + relativedelta(months=-1)
    }
    total_objects = queryset
    total_objects_past_week = total_objects.filter(
        **week_kwargs
    )
    total_objects_past_month = total_objects.filter(
        **month_kwargs
    )
    total_objects_previous_month = total_objects.filter(
        **previous_kwargs
    )

    total_objects_count = total_objects.count()
    total_objects_past_week_count = total_objects_past_week.count()
    total_objects_past_month_count = total_objects_past_month.count()
    total_objects_previous_month_count = total_objects_previous_month.count()
    try:
        percent_change = ((total_objects_past_month_count - \
                           total_objects_previous_month_count) \
                          / float(total_objects_previous_month_count)) * 100
    except ZeroDivisionError:
        percent_change = 0.0

    _push_total_week_month(
        api_key,
        total_objects_count,
        total_objects_past_week_count,
        total_objects_past_month_count,
        percent_change
    )


def push_registrations():
    API_KEY = '62f6d19214ff4f52aa36b8e80295461c'

    _push_total(
        API_KEY,
        get_user_model().objects.all(),
        'date_joined'
    )


def push_comments():
    API_KEY = '6afd86c1d40a4f52b0ccc8f2b7a71050'

    _push_total(
        API_KEY,
        comment_models.CommentModel.objects.all(),
        'publish_at'
    )


def push_likes():
    API_KEY = 'd3de5ac4dce3478d840158b958f574b0'

    _push_total(
        API_KEY,
        tunosocial_models.Like.objects.all(),
        'created_at'
    )


def push_research_tool_polls():
    API_KEY = 'd3de5ac4dce3478d840158b958f574b0'

    _push_total(
        API_KEY,
        preferences.SitePreferences.research_tool.poll.answers.all(),
        'publish_at'
    )
