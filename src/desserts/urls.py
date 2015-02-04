
from django.conf.urls import patterns, include, url

from desserts import views

urlpatterns = patterns('',
        url(r'^$', views.desserts),
)
