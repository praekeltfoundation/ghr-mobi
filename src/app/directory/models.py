'''
Created on 21 Oct 2013

@author: michael
'''
from django.db import models

from tunobase.core import models as core_models

class DirectoryCategory(core_models.StateModel, core_models.SlugModel):
    
    class Meta:
        verbose_name_plural = 'directory categories'
    
    def __unicode__(self):
        return u'%s' % self.title
    
class DirectoryItem(core_models.StateModel, core_models.SlugModel):
    category = models.ForeignKey(DirectoryCategory, related_name='directory_items')
    address = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255)
    tel_number = models.CharField(max_length=16, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    def __unicode__(self):
        return u'%s' % self.name
