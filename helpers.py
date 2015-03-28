from os import remove
from re import search
from subprocess import Popen
from datetime import datetime
from fileinput import FileInput
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import APIException
from eszone_ipf.settings import CONF_DIR, LOG_CONF


class MyException(APIException):
    status_code = 404
    default_detail = 'This is a bug'


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
        return e

def get_status():
    try:
        return 'online'
        #return Popen('svcs ipfilter | tail -n 1 | cut -d " " -f1').read()
    except Exception as e:
        return e

def change_state(arg):
    try:
        return arg
        #return Popen('svcadm {} ipfilter'.format(arg)).read()
    except Exception as e:
        return e

def get_log():
    try:
        with open(LOG_CONF) as conf:
            for line in conf.readlines():
                if search('local0.debug', line):
                    with open(line.split('\t')[-1]) as log:
                        return log.read()

        # bash find file alternative
        # file = Popen("grep local0.debug LOG_CONF | cut -f2 -d$'\t'").read()
    except Exception as e:
        return e

def modify_log(arg):
    try:
        for line in FileInput(LOG_CONF, inplace=1):
            if search('local0.debug', line):
                #/var/log/{}
                print 'local0.debug\t/root/Desktop/bp/other/{}'.format(arg),
                with open('/root/Desktop/bp/other/{}'.format(arg), 'w+') as f:
                    f.write('#ipf log\n#created: {}\n'.format(datetime.now()))
                #Popen('svcadm restart system-log')
                return
            print line,

        #sed alternative
        #Popen("sed -i 's/local0.debug\t\/var\/log\/.*/local0.debug\t\/var\/log\/{}/g' {}".format(arg, LOF_CONF)
    except Exception as e:
        return e