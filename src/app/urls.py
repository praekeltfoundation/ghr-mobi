from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^authentication/', include('app.authentication.urls')),
    (r'^articles/', include('app.articles.urls')),
#     (r'^contacts/', include('app.contacts.urls')),
    (r'^directory/', include('app.directory.urls')),
    (r'^discussions/', include('app.discussions.urls')),
#     (r'^faq/', include('app.faq.urls')),
    (r'^galleries/', include('app.galleries.urls')),
#     (r'^newsfeed/', include('app.newsfeed.urls')),
#     (r'^research-tool/', include('app.research_tool.urls')),
    (r'^', include('app.root.urls')),
)