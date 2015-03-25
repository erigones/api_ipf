from os import remove
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from subprocess import Popen
from eszone_ipf.settings import CONF_DIR

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def get_content(title):
    try:
        with open(''.join([CONF_DIR, title]), 'rb') as f:
            return f.read()
    except Exception as e:
        return e

def file_delete(title):
    try:
        remove(''.join([CONF_DIR, title]))
    except Exception as e:
        print(e)

def get_status():
    try:
        return 'online'
        #return Popen('svcs ipfilter | tail -n 1 | cut -d " " -f1').read()
    except Exception as e:
        return e

def enable_firewall():
    try:
        return 'enabled'
        #return Popen('svcadm enable ipfilter').read()
    except Exception as e:
        print(e)
        return e

def disable_firewall():
    try:
        return 'disabled'
        #return Popen('svcadm disable ipfilter').read()
    except Exception as e:
        print(e)
        return e