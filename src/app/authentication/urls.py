'''
Certain sections of the authentication module originates from django-registration
https://bitbucket.org/ubernostrum/django-registration

Copyright (c) 2007-2012, James Bennett
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.
    * Neither the name of the author nor the names of other
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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
        views.ProjectPasswordReset.as_view(
            template_name='authentication/password_reset_form.html',
            form_class=forms.ProjectPasswordResetForm
        ),
        name='secure_password_reset'
    ),
                       
    url(r'^password_reset/done/$',
        TemplateView.as_view(
            template_name='authentication/password_reset_done.html'
        ),
        name='password_reset_done'
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