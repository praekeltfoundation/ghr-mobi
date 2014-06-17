'''
Created on 22 Oct 2013

@author: michael
'''
from django.contrib import admin

from app.root import models

admin.site.register(models.Visitor)
admin.site.register(models.PageImpression)
