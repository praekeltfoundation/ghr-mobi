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
        fields = ("username",)
        
    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            models.EndUser.objects.get(username=username)
        except models.EndUser.DoesNotExist:
            return username
        raise forms.ValidationError("A user with that username already exists.")

class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = models.EndUser
        
    def is_valid(self):
        """
        Returns True if the form has no errors. Otherwise, False. If errors are
        being ignored, returns False.
        """
        
        return self.is_bound and not bool(self.errors)
    
class CustomUserAdmin(UserAdmin):
    search_fields = ('username', 'mobile_number')
    list_display = ('username', 'mobile_number', 'is_admin', 'is_active', 'is_staff','gender', 'Date_of_birth')
    list_filter = ('username', 'mobile_number', 'is_admin', 'is_active')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('image', 'mobile_number', 'last_login','gender')}),
        (_('Permissions'), {'fields': ('is_superuser', 'is_active', 'is_admin', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )
    
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

admin.site.register(models.EndUser, CustomUserAdmin)