'''
Created on 21 Oct 2013

@author: michael
'''
from django.dispatch import Signal, receiver
from django.conf import settings

from registration import signals as registration_signals

from app.authentication import tasks

# A contact message has been saved
password_was_reset = Signal(providing_args=["sender", "context"])
        
@receiver(password_was_reset)
def password_reset(sender, **kwargs):
    context = kwargs.pop('context', None)
    
    if context is not None:
        if settings.USE_CELERY:
            tasks.sms_password_reset.delay(context)
        else:
            tasks.sms_password_reset(context)