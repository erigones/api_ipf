from os import remove, rename
from subprocess import Popen
from django.http import HttpResponse
from eszone_ipf.settings import BCK_DIR, CONF_DIR, LOG_DIR
from rest_framework.renderers import JSONRenderer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def file_content(path):
    try:
        with open(path, 'rb') as f:
            return f.read()
    except Exception as e:
        return e


def file_delete(path):
    try:
        remove(path)
    except Exception as e:
        return e

def add_pool(path):
    try:
        if not Popen('ippool -f {}'.format(path)):
            return('Ippool added.')
    except Exception as e:
        return e


def activate_config(path, type):
    bck_path = ''.join([BCK_DIR, 'conf.bck'])

    try:
        rename(path, bck_path)
        if type == 'ipf' and not Popen('ipf -Fa -f {}'.format(path)).read():
            return('Configuration activated.')
        elif type == 'nat' and not Popen('ipnat -FC -f {}'.format(path)).read():
            return('Configuration activated.')
    except Exception as e:
        rename(bck_path, path)
        return e