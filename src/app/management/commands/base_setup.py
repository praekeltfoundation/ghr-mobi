'''
Created on 16 Jan 2013

@author: euan
'''
from django.core.management.base import BaseCommand
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