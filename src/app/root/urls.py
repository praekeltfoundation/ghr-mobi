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
                       
    url(r'^register/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/register.html',
        ),
        name='register'
    ),
                       
    url(r'^login/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/login.html',
        ),
        name='login'
    ),
                       
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
                       
    url(r'^my_profile/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/my_profile.html',
        ),
        name='my_profile'
    ),
                       
    url(r'^my_profile_edit/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/my_profile_edit.html',
        ),
        name='my_profile_edit'
    ),       
                       
    url(r'^my_profile_public/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/my_profile_public.html',
        ),
        name='my_profile_public'
    ), 
                       
    url(r'^articles/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/list_view.html',
        ),
        name='articles'
    ),    
                       
    url(r'^galleries/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/galleries.html',
        ),
        name='galleries'
    ),      
                       
    url(r'^gallery/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/gallery_detail.html',
        ),
        name='gallery'
    ),              
                       
    url(r'^discussions/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/discussions.html',
        ),
        name='discussions'
    ),              
                       
    url(r'^directory/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/directory.html',
        ),
        name='directory'
    ),              
                       
    url(r'^directory_detail/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/directory_detail.html',
        ),
        name='directory_detail'
    ),                
                       
    url(r'^faq/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/faq.html',
        ),
        name='faq'
    ),              
                       
    url(r'^faq_detail/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/faq_detail.html',
        ),
        name='faq_detail'
    ),               
                       
    url(r'^contact_category/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/contact_category.html',
        ),
        name='contact_category'
    ),            
                       
    url(r'^contact_category_detail/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/contact_category_detail.html',
        ),
        name='contact_category_detail'
    ),              
                       
    url(r'^newsfeed/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/newsfeed.html',
        ),
        name='newsfeed'
    ),               
                       
    url(r'^newsfeed_detail/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/newsfeed_detail.html',
        ),
        name='newsfeed_detail'
    ),                  
                       
    url(r'^research_tool/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/research_tool.html',
        ),
        name='research_tool'
    ),               
                       
    url(r'^research_tool_results/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/research_tool_results.html',
        ),
        name='research_tool_results'
    ),
                       
    url(r'^contact/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/contact.html',
        ),
        name='contact'
    ),  
                       
    url(r'^terms/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/terms.html',
        ),
        name='terms'
    ),   
                       
    url(r'^privacy/$',
        generic_views.TemplateView.as_view(
            template_name='ghr/privacy.html',
        ),
        name='privacy'
    ),    
    
)