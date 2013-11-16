'''
Created on 28 Oct 2013

@author: michael
'''
from django import forms

from tunobase.bulk_loading import forms as bulk_loading_forms

class ArticleBulkUploadValidatorForm(bulk_loading_forms.BulkUploadValidatorForm):
    title = forms.CharField(max_length=255)
    plain_content = forms.CharField(max_length=255)