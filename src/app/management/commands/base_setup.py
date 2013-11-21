'''
Created on 16 Jan 2013

@author: euan
'''
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site

#==============================================================================
class Command(BaseCommand):
    """
    Initial base setup
    """
    #--------------------------------------------------------------------------
    def handle(self, *args, **options):
        # Sites
        print 'Defaulting site to localhost:8000'
        site = Site.objects.get_current()
        site.domain = 'localhost:8000'
        site.name = 'localhost'
        site.save()
        
        print 'Creating Groups'
        Group.objects.create(name='Ni Nyampinga Journalists')
        Group.objects.create(name='Ambassadors')
        
        print 'Creating Flatpages'
        site = Site.objects.get_current()
        terms = FlatPage.objects.create(
            url='/terms/',
            title='Terms & Conditions',
            content='<p>Terms &amp; Conditions</p>'
        )
        terms.sites.add(site)
        
        privacy_policy = FlatPage.objects.create(
            url='/privacy/',
            title='Privacy Policy',
            content='<p>Privacy Policy</p>'
        )
        privacy_policy.sites.add(site)
        
        contact = FlatPage.objects.create(
            url='/contact/',
            title='Contact Us',
            content='<p>Contact Us</p>'
        )
        contact.sites.add(site)