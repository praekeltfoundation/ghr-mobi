'''
Created on 22 Oct 2013

@author: michael
'''
from django.contrib import admin

from app.faq import models

admin.site.register(models.FAQ)
