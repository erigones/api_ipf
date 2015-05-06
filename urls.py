from django.conf.urls import patterns, url
from api_ipf import settings, views

urlpatterns = patterns('api_ipf.views',
    url(r'^config/$', views.config),
    url(r'^config/(?P<title>.+)/$', views.config_detail),
    url(r'^log/$', views.log),
    url(r'^log/(?P<title>.+)/$', views.log_detail),
    url(r'^command/(?P<args>.+)/$', views.other_commands),
)