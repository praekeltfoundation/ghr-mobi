'''
Created on 21 Oct 2013

@author: michael
'''
from celery.decorators import task

from django.contrib.sites.models import Site
from django.conf import settings
from django.template.loader import render_to_string

@task(default_retry_delay=10 * 60)
def email_account_activation(registration_profile_id, site_id):
    try:
        from unomena.auth import models
        registration_profile = models.ProjectRegistrationProfile.objects.get(pk=registration_profile_id)
        site = Site.objects.get(pk=site_id)
        
        ctx_dict = {
            'user' : registration_profile.user,
            'activation_key': registration_profile.activation_key,
            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
            'site': site,
            'app_name': settings.APP_NAME
        }
            
        subject = render_to_string(
            'auth/activation_email_subject.txt',
            ctx_dict
        )
        
        text_content = render_to_string(
            'auth/activation_email.txt',
            ctx_dict
        )
        
#         email_utils.send_mail('registration/activation_email.html', ctx_dict, subject,
#                         text_content, settings.DEFAULT_FROM_EMAIL, [registration_profile.user.email,])
    except Exception, exc:
        raise email_account_activation.retry(exc=exc)