'''
Created on 21 Oct 2013

@author: michael
'''
from django.db.models.signals import post_save
from django.dispatch import receiver

from registration import signals as registration_signals

from unomena.auth import models, mailer

@receiver(registration_signals.user_registered)
def registration_profile_created(sender, **kwargs):
    print sender, kwargs