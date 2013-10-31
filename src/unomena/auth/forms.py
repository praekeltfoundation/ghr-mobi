from django.conf import settings
from django import forms
from django.contrib.sites.models import get_current_site
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.template import loader
from django.utils.http import int_to_base36
from django.template.loader import render_to_string

from . import constants

# Registration forms

class ProjectRegistrationForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.
    
    """
    title = forms.ChoiceField(choices=constants.TITLE_CHOICES)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=75)
    phone = forms.CharField(max_length=16, required=False)
    mobile = forms.CharField(max_length=16, required=False)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.

        """
        User = get_user_model()
        try:
            if User.objects.get(email__exact=self.cleaned_data['email']):
                raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        except User.DoesNotExist:
            return self.cleaned_data['email']

    def clean_password2(self):
        """
        Verify that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] and self.cleaned_data['password2']:
                if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                    raise forms.ValidationError('The password fields didn\'t match: Password confirmation failed.')
            return self.cleaned_data['password2']

    def clean(self):
        """
        Verify that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] and self.cleaned_data['password2']:
                if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                    raise forms.ValidationError('The two password fields didn\'t match.')
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(ProjectRegistrationForm, self).__init__(*args, **kwargs)

        self.user = None

        self.fields['title'].widget.attrs.update({'class':'required'})
        self.fields['first_name'].widget.attrs.update({'class':'required'})
        self.fields['last_name'].widget.attrs.update({'class':'required'})
        self.fields['email'].widget.attrs.update({'class':'required'})
        self.fields['password1'].widget.attrs.update({'class':'required'})
        self.fields['password2'].widget.attrs.update({'class':'required'})
    
class ProjectAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Email address', max_length=75)
    
class ProjectPasswordResetForm(PasswordResetForm):
    
    def save(self, domain_override=None,
             subject_template_name='auth/password_reset_subject.txt',
             email_template_name='auth/password_reset_email.html',
             txt_email_template_name='auth/password_reset_email.txt',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            
            text_content = render_to_string('auth/activation_email.txt', c)
            
#            unobase_utils.send_mail(email_template_name, c, subject, text_content, 
#                            settings.DEFAULT_FROM_EMAIL, [user.email,], None)