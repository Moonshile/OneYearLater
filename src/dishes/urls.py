
from django.conf.urls import patterns, include, url

from dishes import views

urlpatterns = patterns('',
    url(r'^$', views.dishes),
    url(r'^(\d+)/$', views.dishDetail),
)
