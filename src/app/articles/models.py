'''
Created on 21 Oct 2013

@author: michael
'''
from django.db import models
from django.core.urlresolvers import reverse

from tunobase.core import models as core_models
from tunobase.poll import models as poll_models

class Article(core_models.ContentModel):
    poll = models.ForeignKey(
        poll_models.PollQuestion, 
        blank=True, 
        null=True
    )
    
    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug,])
