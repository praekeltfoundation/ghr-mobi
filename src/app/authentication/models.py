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
import re
import datetime

from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
try:
    from django.utils.timezone import now as datetime_now
except ImportError:
    datetime_now = datetime.datetime.now

from photologue.models import ImageModel

SHA1_RE = re.compile('^[a-f0-9]{40}$')

class EndUserManager(BaseUserManager):
    
    def create_user(self, username, password=None, mobile_number=None):
        '''
        Creates and saves a User with the given username and password.
        '''
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            mobile_number=mobile_number
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, username, password):
        '''
        Creates and saves a superuser with the given username and password.
        '''
        user = self.create_user(
            username,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user

class EndUser(ImageModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    mobile_number = models.CharField(max_length=16, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    
    date_joined = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_special_guest = models.BooleanField(default=False)
    
    default_image_category = 'user'
    
    USERNAME_FIELD = 'username'
    
    objects = EndUserManager()
    
    def update(self, **kwargs):
        if kwargs.has_key('mobile'):
            self.mobile_number = kwargs['mobile']

        if kwargs.has_key('password'):
            self.set_password(kwargs['password'])
        else:
            self.set_unusable_password()

        self.save()

    def __unicode__(self):
        return u'%s' % self.username
    
    def get_short_name(self):
        return self.username
    
    @property
    def display_name(self):
        return self.username

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    @property
    def is_ni_nyampinga_journalist(self):
        return self.groups.filter(name='Ni Nyampinga Journalists').exists()
    
    @property
    def is_ambassador(self):
        return self.groups.filter(name='Ambassadors').exists()
    
    @property
    def can_access_console(self):
        "Can the user access the console?"
        return any([self.is_console_user, self.is_superuser, self.is_admin])
    
    def save(self, *args, **kwargs):
        from tunobase.core.models import DefaultImage
        
        if not self.image:
            try:
                self.image = DefaultImage.objects.permitted().get_random(self.default_image_category)
            except:
                pass

        return super(EndUser, self).save(*args, **kwargs)
