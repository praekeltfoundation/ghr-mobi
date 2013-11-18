'''
Created on 22 Oct 2013

@author: michael
'''
from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django import forms

from ckeditor.widgets import CKEditorWidget

from app.root import models

class FlatPageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = FlatPage

class FlatPageAdmin(admin.ModelAdmin):
    form = FlatPageAdminForm
    list_display = ('url', 'title', 'site_list')
    
    def site_list(self, model):
        return ', '.join([site.domain for site in model.sites.all()])

try:
    admin.site.unregister(FlatPage)
except:
    pass

admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(models.SitePreferences)