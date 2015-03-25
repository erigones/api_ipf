from django.conf.urls import patterns, url
from api_ipf import views

urlpatterns = patterns('api_ipf.views',
    url(r'^config/$', views.config),
    url(r'^config/(?P<title>.+)/$', views.config_detail),
    url(r'^fw(?P<arg>.+)?/$', views.firewall),
    url(r'^ipfstat(?P<arg>.+)?/$', views.ipfstat),
    url(r'^ipnat(?P<arg>.+)?/$', views.ipnat),
    url(r'^test/$', views.test),
)