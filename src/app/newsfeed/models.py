'''
Created on 21 Oct 2013

@author: michael
'''
from django.db import models

from tunobase.core import models as core_models


class FeedItem(core_models.ContentModel):
    source_name = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % self.source_name
