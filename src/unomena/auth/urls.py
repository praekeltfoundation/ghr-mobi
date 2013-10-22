'''
Created on 18 Oct 2013

@author: michael
'''
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from django.contrib.admin.views.decorators import staff_member_required

from unomena.auth import views, forms

urlpatterns = patterns('',
    url(r'^secure/activate/(?P<activation_key>\w+)/$', 
        views.ProjectActivation.as_view(template_name='auth/activate.html'),
        name='secure_activate'
    ),
                       
    url(r'^activate/complete/$',
       TemplateView.as_view(template_name='auth/activation_complete.html'),
       name='registration_activation_complete'
    ),
                       
    url(r'^secure/register/$',
        views.ProjectRegistration.as_view(
            template_name='auth/registration_form.html',
            form_class=forms.ProjectRegistrationForm
        ),
        name='secure_register'
    ),
                       
    url(r'^register/complete/$',
        TemplateView.as_view(template_name='auth/registration_complete.html'),
        name='registration_complete'
    ),
                       
    url(r'^register/resend_email/(?P<pk>\d+)/$',
        staff_member_required(
            views.ResendRegistrationEmail.as_view()
        ),
        name='registration_resend_email'
    ),
                       
    url(r'^secure/password_reset/$',
        'django.contrib.auth.views.password_reset', 
        {'password_reset_form' : forms.ProjectPasswordResetForm },
        name='secure_password_reset'
    ),

    url(r'^secure/reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='secure_password_reset_confirm'
    ),
       
    url(r'^secure/login/$',
        views.login,
        {'template_name' : 'auth/login.html' },
        name='secure_login'
    ),
                       
    url(r'^logout/$', 
        views.logout,
        {'template_name' : 'auth/logged_out.html' },
        name='auth_logout'
    )
)