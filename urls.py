from django.conf.urls import patterns, url
from api_ipf import views

urlpatterns = patterns('api_ipf.views',
    url(r'^config/$', views.config),
    url(r'^config/(?P<title>.+)/$', views.config_detail),
    url(r'^ipf(?P<arg>.+)?/$', views.firewall),
    url(r'^stats(?P<arg>.+)?/$', views.statistics),
    url(r'^test/$', views.test),
)