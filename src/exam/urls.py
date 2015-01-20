

from django.conf.urls import patterns, include, url

from exam import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^tags/get/$', views.getTags),
    url(r'^questions/get/$', views.getQuestions),
    url(r'^answer/handin/$', views.handInAnswer),
    url(r'^answer/finish/$', views.finishAnswer),
    url(r'^q/$', views.queryAnswerSheet),
    url(r'^s/$', views.share)
)
