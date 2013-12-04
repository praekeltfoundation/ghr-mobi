'''
Created on 20 Nov 2013

@author: michael
'''
from django.test import TestCase
from django.template.defaultfilters import slugify

from tunobase.core import constants as core_constants

from app.contacts import models

class ContactCategoryModelTestCase(TestCase):
    title = 'Contact Category Model Title'
    contact_title = 'Contact Model Title'
    contact_role = 'Test Role'
    contact_name = 'Test Name'
    contact_tel_number = '012 345 6789'
    contact_email = 'test@example.com'
    slug = slugify(title)

    def setUp(self):
        '''
        Create an Contact Category Model
        '''
        self.contact_category_object = models.ContactCategory.objects.create(
            title=self.title,
        )
        
        models.Contact.objects.create(
            category=self.contact_category_object,
            title=self.contact_title,
            role=self.contact_role,
            name=self.contact_name,
            tel_number=self.contact_tel_number,
            email=self.contact_email
        )

    def test_contact_category_model(self):
        '''
        Test that the Contact Category Model was created, it has at
        least 1 Contact Model and is in the correct state
        '''
        contact_category_object = models.ContactCategory.objects.get(slug=self.slug)
        self.assertEqual(contact_category_object.state, core_constants.STATE_PUBLISHED)
        self.assertGreaterEqual(contact_category_object.contacts, 1)
