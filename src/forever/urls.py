
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from django.conf.urls.static import static

from forever import views

urlpatterns = patterns('',
    url(r'^$', views.index),

    # account
    url(r'^account/', include('account.urls')),
    # dishes
    url(r'^dishes/', include('dishes.urls')),
    # desserts
    url(r'^desserts/', include('desserts.urls')),
    # admin
    url(r'^admin/', include(admin.site.urls)),
)
