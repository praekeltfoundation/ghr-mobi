'''
Created on 21 Oct 2013

@author: michael
'''
from django.db import models
from django.core.urlresolvers import reverse

from tunobase.core import models as core_models


class Discussion(core_models.ContentModel):
    for_ni_nyampinga_journalists_only = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.title
    
    def get_absolute_url(self):
        return reverse('discussion_detail', args=[self.slug,])
