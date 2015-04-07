from os import remove, rename
from django.http import HttpResponse
from eszone_ipf.settings import BCK_DIR
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
        return remove(path)
    except Exception as e:
        return e

def file_move(path, title):
    try:
        rename(path, ''.join([BCK_DIR, title, '.bck']))
    except Exception as e:
        return e