from django.conf import settings
from django import forms
from django.contrib.sites.models import get_current_site
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.template import loader
from django.utils.http import int_to_base36
from django.template.loader import render_to_string
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from app.authentication import signals, constants

# Profile Update Form

class UpdateProfileForm(forms.ModelForm):
    
    class Meta:
        model = get_user_model()
        fields = [
            'username', 'mobile_number', 'image'
        ]
        
    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        
        self.fields['mobile_number'].widget.attrs.update({'class': 'required'})
        self.fields['username'].widget.attrs.update({'readonly': 'readonly'})
        
        
    def clean_username(self):
        '''
        Validate that the supplied email address is unique for the
        site.
        '''
        if get_user_model().objects.filter(username__iexact=self.cleaned_data['username'])\
           .exclude(username__iexact=self.instance.email).exists():
            raise forms.ValidationError(
                'This username is already in use. '
                'Please supply a different username.'
            )
            
        return self.cleaned_data['username']
    
    def clean_mobile_number(self):
        '''
        Validate that the supplied email address is unique for the
        site.
        '''
        if get_user_model().objects.filter(mobile_number__iexact=self.cleaned_data['mobile_number'])\
           .exclude(mobile_number__iexact=self.instance.mobile_number).exists():
            raise forms.ValidationError(
                'This mobile number is already in use. '
                'Please supply a different mobile number.'
            )
            
        return self.cleaned_data['mobile_number']
    
class UpdateProfilePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    
    def __init__(self, user, *args, **kwargs):
        super(UpdateProfilePasswordForm, self).__init__(*args, **kwargs)
        self.user = user
        
    def clean_old_password(self):
        '''
        Verify that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        '''
        if not self.user.check_password(self.cleaned_data['old_password']):
            raise forms.ValidationError('The password supplied does not match your current password.')
                
        return self.cleaned_data['old_password']
        
    def save(self):
        self.user.set_password(self.cleaned_data['password'])
        self.user.save()

# Registration forms

class ProjectRegistrationForm(forms.Form):
    '''
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.
    '''
    username = forms.CharField(max_length=75)
    mobile = forms.CharField(max_length=16, required=False)
    password = forms.CharField(max_length=4, widget=forms.PasswordInput())
    
    def clean_username(self):
        '''
        Validate that the supplied email address is unique for the
        site.
        '''
        if get_user_model().objects.filter(username__iexact=self.cleaned_data['user']).exists():
            raise forms.ValidationError('This username address is already in use. Please supply a different username.')
        
        return self.cleaned_data['username']
    
    def clean_mobile(self):
        '''
        Validate that the supplied email address is unique for the
        site.
        '''
        if get_user_model().objects.filter(mobile_number__iexact=self.cleaned_data['mobile']):
            raise forms.ValidationError(
                'This mobile number is already in use. '
                'Please supply a different mobile number.'
            )
            
        return self.cleaned_data['mobile']

    def __init__(self, *args, **kwargs):
        super(ProjectRegistrationForm, self).__init__(*args, **kwargs)

        self.user = None

        self.fields['username'].widget.attrs.update({'class':'required'})
        self.fields['mobile'].widget.attrs.update({'class':'required'})
        self.fields['password'].widget.attrs.update({'class':'required'})
    
class ProjectAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=75)
    
class ProjectPasswordResetForm(PasswordResetForm):
    
    def save(self, domain_override=None,
             subject_template_name='authentication/password_reset_subject.txt',
             email_template_name='authentication/password_reset_email.html',
             txt_email_template_name='authentication/password_reset_email.txt',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        '''
        Generates a one-use only link for resetting password and sends to the
        user.
        '''
        UserModel = get_user_model()
        mobile = self.cleaned_data["mobile"]
        active_users = UserModel._default_manager.filter(
            mobile_number=mobile, is_active=True)
        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not user.has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'mobile': user.mobile_number,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user_id': user.id,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            
            signals.password_was_reset.send(
                sender=self.__class__,
                context=c
            )
            
            