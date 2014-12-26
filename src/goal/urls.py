
from django.conf.urls import patterns, include, url

from goal import views

urlpatterns = patterns('',
        url(r'^$', views.index),
        url(r'^add/$', views.addGoal),
        url(r'^count/$', views.countGoals),
)
