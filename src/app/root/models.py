'''
Created on 21 Oct 2013

@author: michael
'''
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Visitor(models.Model):
    unique = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.timestamp


class PageImpression(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    path = models.CharField(max_length=256)
    user_agent = models.CharField(max_length=256, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(
        ContentType,
        related_name="content_type_set_for_%(class)s",
        blank=True,
        null=True
    )
    object_pk = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    content_object = generic.GenericForeignKey(
        ct_field="content_type",
        fk_field="object_pk"
    )

    def __unicode__(self):
        return u'%s @ %s' % (self.path, self.timestamp)
