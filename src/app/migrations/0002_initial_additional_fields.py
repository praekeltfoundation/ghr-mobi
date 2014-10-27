# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'total_girl_users_metric_api_key'
        db.alter_column(u'preferences_sitepreferences', 'total_girl_users_metric_api_key',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True))

        # Adding field 'top_10_discussions_comments_metric_api_key'
        db.alter_column(u'preferences_sitepreferences', 'top_10_discussions_comments_metric_api_key',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True))
        
        # Adding field 'top_10_discussions_comments_metric_api_key'
        db.alter_column(u'preferences_sitepreferences', 'total_unique_and_registration_user_metric_api_key',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True))

    def backwards(self, orm):
        # Deleting field 'total_girl_users_metric_api_key'
        db.alter_column(u'preferences_sitepreferences', 'total_girl_users_metric_api_key',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True))

        # Deleting field 'top_10_discussions_comments_metric_api_key'
        db.alter_column(u'preferences_sitepreferences', 'top_10_discussions_comments_metric_api_key',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True))

        # Deleting field 'total_unique_and_registration_user_metric_api_key'
        db.alter_column(u'preferences_sitepreferences', 'total_unique_and_registration_user_metric_api_key',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True))

    models = {
        
    }

    complete_apps = ['app']