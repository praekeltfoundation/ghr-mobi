from django.contrib import admin

# Register your models here.
from django.contrib import admin

from app.experts import models

admin.site.register(models.ExpertOpinion)