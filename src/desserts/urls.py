
from django.conf.urls import patterns, include, url

from desserts import views

urlpatterns = patterns('',
        url(r'^$', views.desserts),
        url(r'^bowl/$', views.bowl),
        url(r'^add/$', views.add),
        url(r'^rm/$', views.remove),
        url(r'^todo/$', views.todo),
        url(r'^done/$', views.done),
)
