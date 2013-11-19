'''
Created on 21 Oct 2013

@author: michael
'''
from django.db import models

from tunobase.core import models as core_models

class Discussion(core_models.StateModel, core_models.SlugModel, core_models.AuditModel):
    
    def __unicode__(self):
        return u'%s' % self.title

