'''
Created on 21 Oct 2013

@author: michael
'''
from django.db import models

from tunobase.core import models as core_models

class ContactCategory(core_models.StateModel, core_models.SlugModel):
    
    class Meta:
        verbose_name_plural = 'Ni Nyampinga Contact categories'
    
    def __unicode__(self):
        return u'%s' % self.title
    
class Contact(core_models.StateModel, core_models.SlugModel):
    category = models.ForeignKey(ContactCategory, related_name='contacts')
    role = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    tel_number = models.CharField(max_length=16, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Ni Nyampinga Contacts'
    
    def __unicode__(self):
        return u'%s' % self.name
