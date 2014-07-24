'''
Created on 21 Oct 2013

@author: michael
'''
from django.db import models

from tunobase.core import models as core_models
from tunobase.poll import models as poll_models

class Article(core_models.ContentModel):
    summary = models.TextField(validators=[MaxLengthValidator(100)],blank=True, null=True)
    poll = models.ForeignKey(
        poll_models.PollQuestion, 
        blank=True, 
        null=True
    )

