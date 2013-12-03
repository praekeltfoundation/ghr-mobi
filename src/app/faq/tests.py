'''
Created on 20 Nov 2013

@author: michael
'''
from django.test import TestCase
from django.template.defaultfilters import slugify

from tunobase.core import constants as core_constants

from app.faq import models

class FAQModelTestCase(TestCase):
    title = 'FAQ Model Title'
    slug = slugify(title)

    def setUp(self):
        '''
        Create a FAQ Model
        '''
        self.faq_object = models.FAQ.objects.create(
            title=self.title,
        )

    def test_faq_model(self):
        '''
        Test that the FAQ Model was created and has
        the correct state
        '''
        faq_object = models.FAQ.objects.get(slug=self.slug)
        self.assertEqual(faq_object.state, core_constants.STATE_PUBLISHED)