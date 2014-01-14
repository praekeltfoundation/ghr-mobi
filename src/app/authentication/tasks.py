'''
Created on 21 Oct 2013

@author: michael
'''
from celery.decorators import task

from django.contrib.auth import get_user_model


@task(default_retry_delay=10 * 60)
def sms_password_reset(context):
    try:
        user = get_user_model().objects.get(pk=context['user_id'])

#         mailer_utils.send_mail(
#             subject='email/subjects/password_reset_email_subject.txt',
#             html_content='email/html/password_reset_email.html',
#             text_content='email/txt/password_reset_email.txt',
#             context=context,
#             to_addresses=[user.email,],
#             user=user
#         )
    except Exception, exc:
        raise sms_password_reset.retry(exc=exc)
