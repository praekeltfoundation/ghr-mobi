'''
Created on 27 Jan 2014

@author: euan
'''
from django import forms

from tunobase.core.models import ContentModel

from app.discussions.models import Discussion

class SearchForm(forms.Form):
    search_criteria = forms.CharField(widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['search_criteria'].widget.attrs.update(
            {
             'placeholder':'Enter your search criteria here',
             'class':'required',
             'rows':'1'
            }
        )
    
    def search(self):
        phrase = self.cleaned_data['search_criteria'].strip()
        restricted_ids = Discussion.objects.filter(for_ni_nyampinga_journalists_only=True).values_list('id', flat=True)
        results = ContentModel.objects.filter(title__icontains=phrase).exclude(id__in=restricted_ids)
        return results, results.count(), phrase