'''
Created on 20 Nov 2013

@author: michael
'''
from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError

from app.authentication import models

class EndUserModelTestCase(TestCase):
    username = 'user'
    super_user_username = 'superuser'

    def setUp(self):
        '''
        Create an End User Model
        '''
        self.end_user_object = models.EndUser.objects.create_user(
            username=self.username,
            password='1234'
        )
        
        self.end_user_object = models.EndUser.objects.create_superuser(
            username=self.super_user_username,
            password='1234'
        )

    def test_end_user_model(self):
        '''
        Test that the End User was created successfully
        and that no duplicates of the same email address
        are allowed
        '''
        end_user_object = models.EndUser.objects.get(username=self.super_user_username)
        self.assertTrue(end_user_object.is_active)
        self.assertLessEqual(end_user_object.date_joined, timezone.now())
        
        try:
            duplicate_end_user = models.EndUser.objects.create_user(
                username=self.username,
                password='1234'
            )
        except IntegrityError:
            duplicate_end_user = None
        self.assertIsNone(duplicate_end_user, "Duplicate End User was created")
        
    def test_super_end_user_model(self):
        '''
        Test that the Super End User was created successfully
        '''
        super_end_user_object = models.EndUser.objects.get(username=self.super_user_username)
        self.assertTrue(super_end_user_object.is_admin)
        self.assertTrue(super_end_user_object.is_superuser)
