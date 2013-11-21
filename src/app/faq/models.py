'''
Created on 21 Oct 2013

@author: michael
'''
from django.db import models

from tunobase.core import models as core_models
    
class FAQ(core_models.ContentModel):
    
    class Meta:
        verbose_name_plural = 'Frequently Asked Questions'
