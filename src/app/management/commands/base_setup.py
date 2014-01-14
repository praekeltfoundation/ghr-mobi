'''
Created on 16 Jan 2013

@author: euan
'''
from optparse import make_option

from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from django.contrib.flatpages.models import FlatPage
from django.db.utils import IntegrityError


class Command(BaseCommand):
    """
    Initial base setup
    """
    option_list = BaseCommand.option_list + (
        make_option(
            '--site',
            action='store',
            type="string",
            dest='site',
            default='localhost:8000',
            help='Set the default site'
        ),
    )

    def handle(self, *args, **options):
        # Sites
        print 'Defaulting site to %s' % options['site']
        site = Site.objects.get_current()
        site.domain = options['site']
        site.name = 'Default Site'
        site.save()

        print 'Creating Groups'
        _, created = Group.objects.get_or_create(
            name='Ni Nyampinga Journalists'
        )
        if not created:
            print 'Journalists already exist'

        _, created = Group.objects.get_or_create(
            name='Ambassadors'
        )
        if not created:
            print 'Ambassadors already exist'

        print 'Creating Flatpages'
        site = Site.objects.get_current()
        terms, _ = FlatPage.objects.get_or_create(
            url='/terms/',
            title='Terms & Conditions',
            content='<p>Terms &amp; Conditions</p>'
        )
        terms.sites.add(site)

        privacy_policy, _ = FlatPage.objects.get_or_create(
            url='/privacy/',
            title='Privacy Policy',
            content='<p>Privacy Policy</p>'
        )
        privacy_policy.sites.add(site)

        contact, _ = FlatPage.objects.get_or_create(
            url='/contact/',
            title='Contact Us',
            content='<p>Contact Us</p>'
        )
        contact.sites.add(site)
