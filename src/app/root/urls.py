from django.conf.urls import patterns, include, url
from django.contrib.flatpages.views import flatpage

from tunobase.age_gate.decorators import age_gated

from app.root import views

urlpatterns = patterns('',
    url(r'^$',
        views.Index.as_view(
            template_name='root/index.html',
        ),
        name='index'
    ),
                       
    url(r'^about/$', 
        age_gated(flatpage), 
        {'url': '/about/'}, 
        name='about'
    ),
)