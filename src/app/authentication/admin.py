'''
Created on 18 Oct 2013

@author: michael
'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm,
    AdminPasswordChangeForm)
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.safestring import mark_safe

from app.authentication import models
    
class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = models.EndUser
        fields = ("email",)
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].required = False
        
    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            models.EndUser.objects.get(email=email)
        except models.EndUser.DoesNotExist:
            return email
        raise forms.ValidationError("A user with that email address already exists.")
        
    def clean_username(self):
        return self.cleaned_data["username"]

class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = models.EndUser
        
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].required = False
        
    def is_valid(self):
        """
        Returns True if the form has no errors. Otherwise, False. If errors are
        being ignored, returns False.
        """
        print self.errors
        
        return self.is_bound and not bool(self.errors)
    
class CustomUserAdmin(UserAdmin):
    search_fields = ('first_name', 'last_name', 'email')
    list_display = ('email', 'username', 'password', 'first_name', 'last_name', 'is_admin', 'is_active', 'is_staff', 'is_console_user')
    list_filter = ('email', 'username', 'password', 'first_name', 'last_name', 'is_admin', 'is_active')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('image', 'title', 'first_name', 'last_name', 'phone_number', 'mobile_number', 'company', 'city', 'last_login')}),
        (_('Permissions'), {'fields': ('is_superuser', 'is_active', 'is_admin', 'is_console_user', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    
class ProjectRegistrationProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'resend_email')
    search_fields = ('user__email',)
    
    def resend_email(self, model):
        return mark_safe('<a href="%s">Resend email</a>' % reverse('registration_resend_email', args=(model.pk,)))

admin.site.register(models.EndUser, CustomUserAdmin)
admin.site.register(models.ProjectRegistrationProfile, ProjectRegistrationProfileAdmin)