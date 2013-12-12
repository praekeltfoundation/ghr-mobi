'''
Created on 21 Oct 2013

@author: michael
'''
import random

from celery.decorators import task

from django.contrib.sites.models import Site
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from tunobase.api.vumi import vumi_api


@task(default_retry_delay=10 * 60)
def sms_password_reset(user_id):
    try:
        user = get_user_model().objects.get(pk=user_id)
        new_password = str(random.randint(1000, 9999))
        user.set_password(new_password)
        user.save()

        vumi_api.send_sms(
            'Your new GHR PIN is %s' % new_password,
            [user.mobile_number]
        )
    except Exception, exc:
        raise sms_password_reset.retry(exc=exc)
