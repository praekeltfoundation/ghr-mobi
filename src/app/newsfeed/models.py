'''
Created on 21 Oct 2013

@author: michael
'''
from django.db import models
from django.core.urlresolvers import reverse

from tunobase.core import models as core_models
    
class FeedItem(core_models.ContentModel):
    source_name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return u'%s' % self.source_name
    
    def get_absolute_url(self):
        return reverse('newsfeed_detail', args=[self.slug,])