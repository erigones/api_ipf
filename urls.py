from django.conf.urls import patterns, url
from api_ipf import views

urlpatterns = patterns('api_ipf.views',
    url(r'^config/$', views.config),
    url(r'^config/(?P<title>.+)/$', views.config_detail),
    url(r'^activate/(?P<title>.+)/$', views.config_activate),
    url(r'^log/$', views.log),
    url(r'^log/(?P<title>.+)/$', views.log_detail),
    url(r'^update/$', views.blacklist),
    url(r'^command/(?P<args>.+)/$', views.other_commands),
)