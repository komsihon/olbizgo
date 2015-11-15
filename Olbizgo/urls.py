from Olbizgo.views import Theme
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^', include('amazon.urls', namespace='amazon')),
    url(r'^theme/$', Theme.as_view()),

    url(r'^alino/', include(admin.site.urls)),
)
