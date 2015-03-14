
from django.conf.urls import patterns, include, url

from account import views

urlpatterns = patterns('',
    url(r'^$', views.account),
    url(r'^signin/$', views.signin),
    url(r'^signup/$', views.signup),
)
