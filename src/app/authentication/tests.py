'''
Certain sections of the authentication module originates from django-registration
https://bitbucket.org/ubernostrum/django-registration

Copyright (c) 2007-2012, James Bennett
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.
    * Neither the name of the author nor the names of other
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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

    def test_random_image_assignment(self):
        default_image = DefaultImage.objects.permitted().get_random('user')

        self.assertIsNotNone(default_image, "Default image not set")
