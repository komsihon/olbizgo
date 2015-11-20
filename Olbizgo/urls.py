from Olbizgo.views import Theme
from cms.views import FlatPageView
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^', include('amazon.urls', namespace='amazon')),
    url(r'^page/(?P<slug>[-\w]+)/', FlatPageView.as_view(), name='flat_page'),
    url(r'^theme/$', Theme.as_view()),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^alino/', include(admin.site.urls)),
)
