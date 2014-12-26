from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'forever.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # goal
    url(r'^goal/', include('goal.urls')),

    # admin
    url(r'^admin/', include(admin.site.urls)),
)
