'''
Created on 20 Nov 2013

@author: michael
'''
from django.test import TestCase
from django.template.defaultfilters import slugify

from tunobase.core import constants as core_constants

from app.discussions import models

class DiscussionModelTestCase(TestCase):
    title = 'Discussion Model Title'
    slug = slugify(title)

    def setUp(self):
        '''
        Create a Discussion Model
        '''
        self.discussion_object = models.Discussion.objects.create(
            title=self.title,
        )

    def test_discussion_model(self):
        '''
        Test that the Discussion Model was created and has
        the correct state
        '''
        discussion_object = models.Discussion.objects.get(slug=self.slug)
        self.assertEqual(discussion_object.state, core_constants.STATE_PUBLISHED)
        discussion_object.for_ni_nyampinga_journalists_only = True
        discussion_object.save()
        self.assertTrue(discussion_object.for_ni_nyampinga_journalists_only)