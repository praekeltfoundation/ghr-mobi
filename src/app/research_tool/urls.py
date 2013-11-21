'''
Created on 18 Oct 2013

@author: michael
'''
from django.conf.urls import patterns, url

from app.research_tool import views

urlpatterns = patterns('',
                       
    url(r'^$', 
        views.ResearchTool.as_view(
            template_name='research_tool/research_tool.html'
        ),
        name='research_tool'
    ),
)