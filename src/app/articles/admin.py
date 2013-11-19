'''
Created on 22 Oct 2013

@author: michael
'''
from django.contrib import admin

from app.articles import models

admin.site.register(models.Article)