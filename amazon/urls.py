from amazon.views import Home, Links, ItemList, add_subscriber
from django.conf.urls import patterns, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^boutique/(?P<category_slug>[-\w]+)/$', ItemList.as_view(), name='item_list'),
    url(r'^boutique/$', ItemList.as_view(), name='item_list'),
    url(r'^add_subscriber$', add_subscriber, name='add_subscriber'),
    url(r'^liens/$', Links.as_view()),
)
