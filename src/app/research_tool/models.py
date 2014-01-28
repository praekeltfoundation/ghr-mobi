'''
Created on 21 Oct 2013

@author: michael
'''
from django.db import models
from django.core.urlresolvers import reverse

from tunobase.core import models as core_models
from tunobase.poll import models as poll_models

class ResearchTool(core_models.ContentModel):
    poll = models.OneToOneField(
        poll_models.PollQuestion
    )
    
    def get_absolute_url(self):
        return reverse('research_tool_detail', args=[self.slug,])

