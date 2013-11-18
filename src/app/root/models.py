'''
Created on 21 Oct 2013

@author: michael
'''
from django.db import models

from preferences.models import Preferences

from tunobase.poll import models as poll_models

class SitePreferences(Preferences):
    __module__ = 'preferences.models'
    
    active_poll = models.ForeignKey(poll_models.PollQuestion, blank=True, null=True)