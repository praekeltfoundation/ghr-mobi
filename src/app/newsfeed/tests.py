'''
Created on 20 Nov 2013

@author: michael
'''
from django.test import TestCase
from django.template.defaultfilters import slugify

from tunobase.core import constants as core_constants

from app.newsfeed import models

class FeedItemModelTestCase(TestCase):
    title = 'Feed Item Model Title'
    source_name = 'Test Source Name'
    slug = slugify(title)

    def setUp(self):
        '''
        Create a Feed Item Model
        '''
        self.feed_item_object = models.FeedItem.objects.create(
            title=self.title,
            source_name=self.source_name
        )

    def test_feed_item_model(self):
        '''
        Test that the Feed Item Model was created and has
        the correct state
        '''
        feed_item_object = models.FeedItem.objects.get(slug=self.slug)
        self.assertEqual(feed_item_object.state, core_constants.STATE_PUBLISHED)
        self.assertEqual(feed_item_object.source_name, self.source_name)