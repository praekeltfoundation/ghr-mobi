'''
Created on 21 Oct 2013

@author: michael
'''
from django.db import models

from preferences.models import Preferences

from tunobase.poll import models as poll_models

from app.research_tool import models as research_tool_models
from app.discussions import models as discussion_models


class SitePreferences(Preferences):
    __module__ = 'preferences.models'

    active_poll = models.ForeignKey(
        poll_models.PollQuestion,
        related_name='active_polls',
        blank=True,
        null=True
    )
    active_discussion = models.ForeignKey(
        discussion_models.Discussion,
        related_name='active_discussions',
        blank=True,
        null=True
    )
    research_tool = models.ForeignKey(
        research_tool_models.ResearchTool,
        blank=True,
        null=True
    )
