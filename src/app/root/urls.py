from django.conf.urls import patterns, include, url
from django.contrib.flatpages.views import flatpage
from django.views import generic as generic_views 

from app.root import views

urlpatterns = patterns('',
    url(r'^$',
        views.Index.as_view(
            template_name='root/index.html',
        ),
        name='index'
    ),
                       
#     url(r'^register/$',
#         generic_views.TemplateView.as_view(
#             template_name='ghr/register.html',
#         ),
#         name='register'
#     ),
#                        
#     url(r'^login/$',
#         generic_views.TemplateView.as_view(
#             template_name='ghr/login.html',
#         ),
#         name='login'
#     ),
                       
    url(r'^forgot_password/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/forgot_password.html',
        ),
        name='forgot_password'
    ),
                       
    url(r'^forgot_password_success/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/forgot_password_success.html',
        ),
        name='forgot_password_success'
    ),
                       
    url(r'^forgot_password_error/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/forgot_password_error.html',
        ),
        name='forgot_password_error'
    ),
                       
    url(r'^search/$',
        generic_views.TemplateView.as_view(
            template_name='root/search.html',
        ),
        name='search'
    ),
    
)