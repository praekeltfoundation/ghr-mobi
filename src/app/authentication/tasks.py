'''
Created on 21 Oct 2013

@author: michael
'''
from celery.decorators import task

from django.contrib.sites.models import Site
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from tunobase.mailer import utils as mailer_utils

@task(default_retry_delay=10 * 60)
def email_account_activation(registration_profile_id, site_id):
    try:
        from app.authentication import models
        registration_profile = models.ProjectRegistrationProfile.objects.get(
            pk=registration_profile_id
        )
        site = Site.objects.get(pk=site_id)
        
        ctx_dict = {
            'user' : registration_profile.user,
            'activation_key': registration_profile.activation_key,
            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
            'site': site,
            'app_name': settings.APP_NAME
        }
        
        print registration_profile.user.email
        
        mailer_utils.send_mail(
            subject='email/subjects/activation_email_subject.txt', 
            html_content='email/html/activation_email.html', 
            text_content='email/txt/activation_email.txt', 
            context=ctx_dict,
            to_addresses=[registration_profile.user.email,],
            user=registration_profile.user
        )
    except Exception, exc:
        raise email_account_activation.retry(exc=exc)
    
@task(default_retry_delay=10 * 60)
def email_password_reset(context):
    try:
        user = get_user_model().objects.get(pk=context['user_id'])
        
        mailer_utils.send_mail(
            subject='email/subjects/password_reset_email_subject.txt', 
            html_content='email/html/password_reset_email.html', 
            text_content='email/txt/password_reset_email.txt', 
            context=context,
            to_addresses=[user.email,],
            user=user
        )
    except Exception, exc:
        raise email_password_reset.retry(exc=exc)