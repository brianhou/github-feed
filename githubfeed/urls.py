from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'githubfeed.views.home', name='home'),
    url(r'^feed/(?P<username>\w*)', 'githubfeed.views.feed', name='feed'),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/rate', 'githubfeed.views.rate', name='rate'),
)
