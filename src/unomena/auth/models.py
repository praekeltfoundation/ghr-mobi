import hashlib
import random
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

from django_countries import CountryField

from photologue.models import ImageModel

from unomena.auth import constants

SHA1_RE = re.compile('^[a-f0-9]{40}$')

class EndUserManager(BaseUserManager):
    
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=EndUserManager.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class EndUser(ImageModel, AbstractBaseUser, PermissionsMixin):
    title = models.CharField(max_length=8, choices=constants.TITLE_CHOICES, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    mobile_number = models.CharField(max_length=16, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    newsletter_recipient = models.BooleanField(default=False)
    
    street_address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state_province = models.CharField(max_length=255, blank=True, null=True)
    zip_postal_code = models.CharField(max_length=8, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    web_address = models.URLField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_console_user = models.BooleanField(default=False)
    
    default_image_category = 'user'
    
    USERNAME_FIELD = 'email'
    
    objects = EndUserManager()
    
    @property
    def display_name(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        
        return self.get_short_name()
    
    def get_full_name(self):
        # The user is identified by their first name and last name
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    @property
    def can_access_console(self):
        "Can the user access the console?"
        return self.is_console_user or self.is_superuser or self.is_admin
    
    def save(self, *args, **kwargs):
        #from unobase.models import DefaultImage
        
        #if not self.image:
        #    self.image = DefaultImage.permitted.get_random(self.default_image_category)

        return super(EndUser, self).save(*args, **kwargs)

class ProjectRegistrationManager(models.Manager):
    
    def activate_user(self, activation_key):
        """
        Validate an activation key and activate the corresponding
        ``User`` if valid.
        
        If the key is valid and has not expired, return the ``User``
        after activating.
        
        If the key is not valid or has expired, return ``False``.
        
        If the key is valid but the ``User`` is already active,
        return ``False``.
        
        To prevent reactivation of an account which has been
        deactivated by site administrators, the activation key is
        reset to the string constant ``RegistrationProfile.ACTIVATED``
        after successful activation.

        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not profile.activation_key_expired():
                user = profile.user
                user.is_active = True
                user.save()
                profile.activation_key = self.model.ACTIVATED
                profile.save()
                return user
        return False
    
    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the address by lowercasing the domain part of the email
        address.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])
        return email
    
    @transaction.commit_on_success
    def create_inactive_user(self, site, send_email=True, **kwargs):
        email = ProjectRegistrationManager.normalize_email(kwargs['email'])
        profile = EndUser.objects.create(
            first_name=kwargs['first_name'], 
            last_name=kwargs['last_name'], 
            email=email,
            is_active=False
        )
        
        if kwargs.has_key('title'):
            profile.title = kwargs['title']
                                         
        if kwargs.has_key('phone'):
            profile.phone_number = kwargs['phone']
            
        if kwargs.has_key('mobile'):
            profile.mobile_number = kwargs['mobile']

        if kwargs.has_key('password1'):
            profile.set_password(kwargs['password1'])
        else:
            profile.set_unusable_password()

        # First save everything before we send signals or emails.
        profile.save()

        registration_profile = self.create_profile(profile)
        
        #if send_email:
        #    automatic_emails.email_account_activation.delay(registration_profile.id, site.id)

        return profile
    
    def create_profile(self, user):
        """
        Create a ``RegistrationProfile`` for a given
        ``User``, and return the ``RegistrationProfile``.
        
        The activation key for the ``RegistrationProfile`` will be a
        SHA1 hash, generated from a combination of the ``User``'s
        username and a random salt.
        
        """
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        username = user.get_username()
        if isinstance(username, unicode):
            username = username.encode('utf-8')
        activation_key = hashlib.sha1(salt+username).hexdigest()
        
        return self.create(user=user, activation_key=activation_key)
    
    def delete_expired_users(self):
        """
        Remove expired instances of ``RegistrationProfile`` and their
        associated ``User``s.
        
        Accounts to be deleted are identified by searching for
        instances of ``RegistrationProfile`` with expired activation
        keys, and then checking to see if their associated ``User``
        instances have the field ``is_active`` set to ``False``; any
        ``User`` who is both inactive and has an expired activation
        key will be deleted.
        
        It is recommended that this method be executed regularly as
        part of your routine site maintenance; this application
        provides a custom management command which will call this
        method, accessible as ``manage.py cleanupregistration``.
        
        Regularly clearing out accounts which have never been
        activated serves two useful purposes:
        
        1. It alleviates the ocasional need to reset a
           ``RegistrationProfile`` and/or re-send an activation email
           when a user does not receive or does not act upon the
           initial activation email; since the account will be
           deleted, the user will be able to simply re-register and
           receive a new activation key.
        
        2. It prevents the possibility of a malicious user registering
           one or more accounts and never activating them (thus
           denying the use of those usernames to anyone else); since
           those accounts will be deleted, the usernames will become
           available for use again.
        
        If you have a troublesome ``User`` and wish to disable their
        account while keeping it in the database, simply delete the
        associated ``RegistrationProfile``; an inactive ``User`` which
        does not have an associated ``RegistrationProfile`` will not
        be deleted.
        
        """
        for profile in self.all():
            try:
                if profile.activation_key_expired():
                    user = profile.user
                    if not user.is_active:
                        user.delete()
                        profile.delete()
            except EndUser.DoesNotExist:
                profile.delete()
    
class ProjectRegistrationProfile(models.Model):
    ACTIVATED = u"ALREADY_ACTIVATED"
    
    user = models.ForeignKey(EndUser, unique=True, verbose_name=_('user'))
    activation_key = models.CharField(_('activation key'), max_length=40)
    
    objects = ProjectRegistrationManager()
    
    class Meta:
        verbose_name = _('registration profile')
        verbose_name_plural = _('registration profiles')
    
    def __unicode__(self):
        return u"Registration information for %s" % self.user
    
    def activation_key_expired(self):
        """
        Determine whether this ``RegistrationProfile``'s activation
        key has expired, returning a boolean -- ``True`` if the key
        has expired.
        
        Key expiration is determined by a two-step process:
        
        1. If the user has already activated, the key will have been
           reset to the string constant ``ACTIVATED``. Re-activating
           is not permitted, and so this method returns ``True`` in
           this case.

        2. Otherwise, the date the user signed up is incremented by
           the number of days specified in the setting
           ``ACCOUNT_ACTIVATION_DAYS`` (which should be the number of
           days after signup during which a user is allowed to
           activate their account); if the result is less than or
           equal to the current date, the key has expired and this
           method returns ``True``.
        
        """
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == self.ACTIVATED or \
               (self.user.date_joined + expiration_date <= datetime_now())
    activation_key_expired.boolean = True