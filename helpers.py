from os import remove
from subprocess import Popen
from django.http import HttpResponse
from api_ipf.settings import CONF_DIR
from rest_framework.renderers import JSONRenderer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = str(JSONRenderer().render(data))
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def file_content(path):
    try:
        with open(path, 'rb') as f:
            return JSONResponse(f.read(), status=200)
    except IOError:
        return JSONResponse('Error: No such file (disk).', status=404)
    except Exception as e:
        return JSONResponse(e, status=400)

def file_delete(obj, path):
    try:
        Popen('pkill ipmon')
        obj.delete()
        remove(path)
        return JSONResponse('Log deleted.', status=204)
    except Exception as e:
        return JSONResponse(e, status=400)

def activate_config(obj):
    path = ''.join([CONF_DIR, obj['title']])

    try:
        if obj['type'] not in ['ipf', 'nat', 'ippool']:
            return JSONResponse('Incorrect type.', status=400)

        elif obj['type'] == 'ippool':
            if not Popen('ippool -f {}'.format(path)).read():
                return JSONResponse('Ippool added.', status=201)
            else:
                return JSONResponse('Incorrect ippool format.', status=400)
    except Exception as e:
        return JSONResponse(e, status=400)

    try:
        if obj['activate'] in ['Y', 'y', 'Yes', 'yes']:

            if obj['type'] == 'ipf':
                if not Popen('ipf -Fa -f {}'.format(path)).read():
                    return JSONResponse('Configuration activated.', status=201)
                else:
                    return JSONResponse('Incorrect ipf format.', status=400)

            elif obj['type'] == 'nat':
                if not Popen('ipnat -FC -f {}'.format(path)).read():
                    return JSONResponse('Configuration activated.', status=201)
                else:
                    return JSONResponse('Incorrect ipf format.', status=400)
        else:
            return JSONResponse('Configuration added.', status=201)

    except Exception as e:
        return JSONResponse(e, status=400)

def realize_command(args):
    try:
        return JSONResponse(args)
        #return JSONResponse(Popen(args).read(), status=200)
    except Exception as e:
        return JSONResponse(e, status=400)
