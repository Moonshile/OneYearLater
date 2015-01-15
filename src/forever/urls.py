
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from django.conf.urls.static import static

from forever import views

urlpatterns = patterns('',
    url(r'^$', views.index),

    # goal
    url(r'^goal/', include('goal.urls')),
    # exam
    url(r'^exam/', include('exam.urls')),

    # admin
    url(r'^admin/', include(admin.site.urls)),
)
