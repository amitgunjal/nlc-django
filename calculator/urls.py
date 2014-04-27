from django.conf.urls import patterns, url
from calculator import views
    
urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    # url(r'^calculate/$', views.calculate, name='calculate'),
)
