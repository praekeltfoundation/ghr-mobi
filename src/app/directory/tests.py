'''
Created on 20 Nov 2013

@author: michael
'''
from django.test import TestCase
from django.template.defaultfilters import slugify

from tunobase.core import constants as core_constants

from app.directory.models import DirectoryCategory, DirectoryItem


class DirectoryCategoryModelTestCase(TestCase):
    title = 'Directory Category Model Title'
    directory_item_title = 'Directory Model Title'
    directory_item_address = 'Directory Item Address'
    directory_item_name = 'Test Directory'
    directory_item_tel_number = '012 345 6789'
    directory_item_email = 'test@example.com'
    slug = slugify(title)
    directory_item_slug = slugify(directory_item_title)

    def setUp(self):
        '''
        Create a Directory Category Model
        '''
        self.directory_category_object = DirectoryCategory.objects.create(
            title=self.title,
        )

        DirectoryItem.objects.create(
            category=self.directory_category_object,
            title=self.directory_item_title,
            address=self.directory_item_address,
            name=self.directory_item_name,
            tel_number=self.directory_item_tel_number,
            email=self.directory_item_email
        )

    def test_directory_category_model(self):
        '''
        Test that the Directory Category Model was created, it has at
        least 1 Directory Item Model and is in the correct state
        '''
        directory_category_object = DirectoryCategory.objects.get(
            slug=self.slug)
        self.assertEqual(directory_category_object.state,
                         core_constants.STATE_PUBLISHED)
        self.assertGreaterEqual(directory_category_object.directory_items, 1)
