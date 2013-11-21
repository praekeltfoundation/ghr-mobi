'''
Created on 22 Oct 2013

@author: michael
'''
from django.contrib import admin

from app.directory import models

admin.site.register(models.DirectoryCategory)
admin.site.register(models.DirectoryItem)