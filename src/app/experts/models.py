from django.db import models

from tunobase.poll import models as poll_models

class ExpertOpinion(models.Model):
    expert_opinion_text = models.CharField(max_length=100, blank=True, null=True)
    poll = models.OneToOneField(
        poll_models.PollQuestion
    )
    def __unicode__(self):
        return u'%s' % self.expert_opinion_text