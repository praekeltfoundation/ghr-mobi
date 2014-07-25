# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'EndUser.total_girl_users_metric_api_key'
        db.add_column(u'preferences_sitepreferences', 'total_girl_users_metric_api_key',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'EndUser.top_10_discussions_comments_metric_api_key'
        db.add_column(u'preferences_sitepreferences', 'top_10_discussions_comments_metric_api_key',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)
        
        # Adding field 'EndUser.top_10_discussions_comments_metric_api_key'
        db.add_column(u'preferences_sitepreferences', 'total_unique_and_registration_user_metric_api_key',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'EndUser.total_girl_users_metric_api_key'
        db.delete_column(u'preferences_sitepreferences', 'total_girl_users_metric_api_key')

        # Deleting field 'EndUser.top_10_discussions_comments_metric_api_key'
        db.delete_column(u'preferences_sitepreferences', 'top_10_discussions_comments_metric_api_key')

        # Deleting field 'EndUser.total_unique_and_registration_user_metric_api_key'
        db.delete_column(u'preferences_sitepreferences', 'total_unique_and_registration_user_metric_api_key')

    models = {
        
    }

    complete_apps = ['app']