'''
Created on 22 Oct 2013

@author: michael
'''
from django.contrib import admin

from app.contacts import models

admin.site.register(models.ContactCategory)
admin.site.register(models.Contact)
