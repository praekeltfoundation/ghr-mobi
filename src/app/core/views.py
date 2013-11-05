'''
Created on 21 Oct 2013

@author: michael
'''
from django.views import generic as generic_views

from tunobase.age_gate import mixins as age_gate_mixins

class Index(age_gate_mixins.AgeGateMixin, generic_views.TemplateView):
    pass