'''
Created on 21 Oct 2013

@author: michael
'''
from django.db.models.signals import post_save
from django.dispatch import receiver

from registration import signals as registration_signals

from unomena.auth import models, mailers

@receiver(registration_signals.user_registered)
def registration_profile_created(sender, **kwargs):
    registration_profile = kwargs.pop('registration_profile', None)
    site = kwargs.pop('site', None)
    send_email = kwargs.pop('send_email', False)
    
    if registration_profile is not None and site is not None and send_email:
        mailers.email_account_activation(registration_profile.id, site.id)