from django.conf.urls import patterns, url
from api_ipf import views


urlpatterns = patterns('api_ipf.views',
    url(r'^config/$', views.config),
    url(r'^config/activate/(?P<title>.+)/$', views.config_activate),
    url(r'^config/(?P<title>.+)/$', views.config_detail),
    url(r'^log/$', views.log),
    url(r'^log/(?P<title>.+)/$', views.log_detail),
    url(r'^update/$', views.blacklist),
    url(r'^ipf/(?P<args>.+)/$', views.ipf),
    url(r'^ipnat/(?P<args>.+)/$', views.ipnat),
    url(r'^ippool/(?P<args>.+)/$', views.ippool),
    url(r'^ipfstat/(?P<args>.+)/$', views.ipfstat),
    url(r'^ipmon/(?P<args>.+)/$', views.ipmon),
    url(r'^svcadm/(?P<args>.+)/$', views.svcadm),
    url(r'^state/(?P<args>.+)/$', views.state),
)
