'''
Created on 18 Oct 2013

@author: michael
'''
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from django.contrib.admin.views.decorators import staff_member_required

from app.authentication import views, forms

urlpatterns = patterns('',
    # Profile stuff
    
    url(r'^user-profile/(?P<pk>\d+)/$', 
        views.UserProfile.as_view(
            template_name='authentication/user_profile.html'
        ),
        name='user_profile'
    ),
    
    url(r'^profile/$', 
        views.Profile.as_view(
            template_name='authentication/profile.html'
        ),
        name='profile'
    ),
    
    url(r'^secure/profile/edit/$', 
        views.UpdateProfile.as_view(
            form_class=forms.UpdateProfileForm,
            template_name='authentication/profile_edit.html'
        ),
        name='secure_profile_edit'
    ),
                       
    url(r'^secure/profile/change_password/$', 
        views.UpdateProfilePassword.as_view(
            form_class=forms.UpdateProfilePasswordForm,
            template_name='authentication/profile_change_password.html'
        ),
        name='secure_profile_change_password'
    ),
                                    
    # Registration and activation
                       
    url(r'^secure/register/$',
        views.ProjectRegistration.as_view(
            template_name='authentication/registration_form.html',
            form_class=forms.ProjectRegistrationForm
        ),
        name='secure_register'
    ),
                       
    url(r'^register/complete/$',
        TemplateView.as_view(
            template_name='authentication/registration_complete.html'
        ),
        name='registration_complete'
    ),
    
    # Authentication
    
    url(r'^secure/password_reset/$',
        'django.contrib.auth.views.password_reset', 
        {
            'template_name': 'authentication/password_reset_form.html',
            'password_reset_form': forms.ProjectPasswordResetForm
        },
        name='secure_password_reset'
    ),

    url(r'^secure/reset/(?P<uidb64>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {
            'template_name': 'authentication/password_reset_confirm.html'
        },
        name='secure_password_reset_confirm'
    ),
                       
    url(r'^password_reset/done/$', 
        'django.contrib.auth.views.password_reset_done', 
        {
            'template_name': 'authentication/password_reset_done.html'
        },
        name='password_reset_done'
    ),
                       
    url(r'^reset/done/$', 
        'django.contrib.auth.views.password_reset_complete', 
        {
            'template_name': 'authentication/password_reset_complete.html'
        },
        name='password_reset_complete'
    ),
       
    url(r'^secure/login/$',
        views.login,
        {'template_name' : 'authentication/login.html'},
        name='secure_login'
    ),
                       
    url(r'^logout/$', 
        views.logout,
        {'template_name' : 'authentication/logged_out.html' },
        name='auth_logout'
    )
)