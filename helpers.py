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

def get_statistics(arg):
    try:
        return Popen('ipstat {}'.format(arg)).read()
    except Exception as e:
        return e

def get_status():
    try:
        return Popen(
            'svcs -x ipfilter:default | grep "State:" | cut -f3 -d " "').read()
    except Exception as e:
        return e

def start_firewall():
    try:
        return Popen('ipfstat enable').read()
    except Exception as e:
        print(e)
        return e

def stop_firewall():
    try:
        return Popen('ipfstat disable').read()
    except Exception as e:
        print(e)
        return e