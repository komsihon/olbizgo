from amazon.views import Home, Links
from django.conf.urls import patterns, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^liens/$', Links.as_view(), name='home'),
)
