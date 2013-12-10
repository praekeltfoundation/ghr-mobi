import random

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from tunobase.api.vumi import vumi_api

import phonenumbers

# Profile Update Form


class UpdateProfileForm(forms.ModelForm):
    password = forms.CharField(
        max_length=4,
        widget=forms.PasswordInput,
        required=False,
        help_text='Leave this blank unless you want to'
    )

    class Meta:
        model = get_user_model()
        fields = [
            'username', 'mobile_number', 'image', 'about_me'
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
        UserModel = get_user_model()
        user_lookup = UserModel.objects.filter(
            username__iexact=self.cleaned_data['username']
        ).exclude(username__iexact=self.instance.username)
        if user_lookup.exists():
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
        try:
            mobile_number = phonenumbers.format_number(phonenumbers.parse(
                self.cleaned_data['mobile_number']
            ), phonenumbers.PhoneNumberFormat.NATIONAL)
        except phonenumbers.phonenumberutil.NumberParseException:
            raise forms.ValidationError(
                'This mobile number is not in the correct format. '
                'Eg +27 71 555 1234.'
            )

        UserModel = get_user_model()
        user_lookup = UserModel.objects.filter(
            mobile_number__iexact=mobile_number
        ).exclude(mobile_number__iexact=self.instance.mobile_number)
        if user_lookup.exists():
            raise forms.ValidationError(
                'This mobile number is already in use. '
                'Please supply a different mobile number.'
            )

        return mobile_number

    def save(self, commit=True):
        obj = super(UpdateProfileForm, self).save(commit=False)
        if self.cleaned_data['password']:
            obj.set_password(self.cleaned_data['password'])
        obj.save()

        return obj


class UpdateProfilePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=4, widget=forms.PasswordInput)
    password = forms.CharField(max_length=4, widget=forms.PasswordInput)

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
            raise forms.ValidationError(
                'The password supplied does not match your current password.')

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
    mobile_number = forms.CharField(
        max_length=16,
        help_text='Should be in the format +27 71 555 1234'
    )
    password = forms.CharField(max_length=4, widget=forms.PasswordInput())

    def clean_username(self):
        '''
        Validate that the supplied email address is unique for the
        site.
        '''
        UserModel = get_user_model()
        user_lookup = UserModel.objects.filter(
            username__iexact=self.cleaned_data['username'])
        if user_lookup.exists():
            raise forms.ValidationError(
                'This username address is already in'
                ' use. Please supply a different username.')

        return self.cleaned_data['username']

    def clean_password(self):
        try:
            int(self.cleaned_data['password'])
        except ValueError:
            raise forms.ValidationError(
                'PIN entered is not a number.'
            )

        return self.cleaned_data['password']

    def clean_mobile_number(self):
        '''
        Validate that the supplied email address is unique for the
        site.
        '''
        try:
            mobile_number = phonenumbers.format_number(phonenumbers.parse(
                self.cleaned_data['mobile_number']
            ), phonenumbers.PhoneNumberFormat.NATIONAL)
        except phonenumbers.phonenumberutil.NumberParseException:
            raise forms.ValidationError(
                'This mobile number is not in the correct format. '
                'Eg +27 71 555 1234.'
            )

        UserModel = get_user_model()
        if UserModel.objects.filter(mobile_number__iexact=mobile_number):
            raise forms.ValidationError(
                'This mobile number is already in use. '
                'Please supply a different mobile number.'
            )

        return mobile_number

    def __init__(self, *args, **kwargs):
        super(ProjectRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'required',
        })
        self.fields['mobile_number'].widget.attrs.update({
            'class': 'required',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'required number',
        })


class ProjectAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=75)


class ProjectPasswordResetForm(forms.Form):
    username = forms.CharField(max_length=75)

    def clean_username(self):
        try:
            username = phonenumbers.format_number(phonenumbers.parse(
                self.cleaned_data['username']
            ), phonenumbers.PhoneNumberFormat.NATIONAL)
        except phonenumbers.phonenumberutil.NumberParseException:
            username = self.cleaned_data['username']

        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(
                Q(username=username) |
                Q(mobile_number=username)
            )
        except UserModel.DoesNotExist:
            raise forms.ValidationError(
                'Username does not exist'
            )

        return user

    def save(self):
        new_password = str(random.randint(1000, 9999))
        user = self.cleaned_data['username']
        user.set_password(new_password)
        user.save()

        # SMS user new pin
        vumi_api.send_sms(
            'Your new GHR PIN is %s' % new_password,
            [user.mobile_number]
        )
