'''
Created on 20 Nov 2013

@author: michael
'''
from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth import authenticate

import phonenumbers

from tunobase.core.models import DefaultImage

from app.authentication import models


class EndUserModelTestCase(TestCase):
    username = 'user'
    mobile_number = '+27 71 555 1234'
    super_user_username = 'superuser'

    def setUp(self):
        '''
        Create an End User Model
        '''
        mobile_number = phonenumbers.format_number(phonenumbers.parse(
            self.mobile_number
        ), phonenumbers.PhoneNumberFormat.NATIONAL)

        self.end_user_object = models.EndUser.objects.create_user(
            username=self.username,
            mobile_number=mobile_number,
            password='1234'
        )


        self.super_end_user_object = models.EndUser.objects.create_superuser(
            username=self.super_user_username,
            password='1234'
        )

    def test_end_user_model(self):
        '''
        Test that the End User was created successfully
        and that no duplicates of the same email address
        are allowed
        '''
        end_user_object = models.EndUser.objects.get(
            username=self.super_user_username
        )
        self.assertTrue(end_user_object.is_active)
        self.assertLessEqual(end_user_object.date_joined, timezone.now())
        self.assertRaises(
            IntegrityError,
            models.EndUser.objects.create_user,
            username=self.username, password='1234'
        )


    def test_super_end_user_model(self):
        '''
        Test that the Super End User was created successfully
        '''
        super_end_user_object = models.EndUser.objects.get(
            username=self.super_user_username
        )
        self.assertTrue(super_end_user_object.is_admin)
        self.assertTrue(super_end_user_object.is_superuser)

    def test_login(self):
        '''
        Test the login functionality with custom backend
        '''
        # authenticate with username
        username_user = authenticate(
            username=self.username,
            password='1234'
        )

        self.assertEqual(username_user.pk, self.end_user_object.pk)

        # authenticate with mobile number
        mobile_user = authenticate(
            username=self.mobile_number,
            password='1234'
        )

        self.assertEqual(mobile_user.pk, self.end_user_object.pk)

