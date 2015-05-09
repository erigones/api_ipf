import os
import sys
import wget
import schedule
import time
import zipfile
from subprocess import Popen
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from api_ipf.settings import *


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


def config_delete(obj, path):
    try:
        obj.delete()
        os.remove(path)
        return JSONResponse('Config deleted.', status=204)
    except Exception as e:
        return JSONResponse(e, status=400)


def log_delete(obj, path):
    try:
        Popen('pkill ipmon')
        obj.delete()
        os.remove(path)
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
                Popen('svcadm refresh ipfilter')
                return JSONResponse('Ippool added.', status=201)
            else:
                return JSONResponse('Incorrect ippool format.', status=400)
    except Exception as e:
        return JSONResponse(e, status=400)

    try:
        if obj['activate'] in ['Y', 'y', 'Yes', 'yes']:

            if obj['type'] == 'ipf':
                if not Popen('ipf -f {}'.format(path)).read():
                    Popen('ipf -Fa -f {}'.format(path))
                    return JSONResponse('Configuration activated.', status=201)
                else:
                    return JSONResponse('Incorrect ipf format.', status=400)

            elif obj['type'] == 'nat':
                if not Popen('ipnat -f {}'.format(path)).read():
                    Popen('ipnat -FC -f {}'.format(path))
                    return JSONResponse('Configuration activated.', status=201)
                else:
                    return JSONResponse('Incorrect ipf format.', status=400)
        else:
            return JSONResponse('Configuration added.', status=201)

    except Exception as e:
        return JSONResponse(e, status=400)


def realize_command(args):
    try:
        if args.split()[0] in ALLOWED_COMMANDS:
            return JSONResponse(args, status=200)
        else:
            return JSONResponse("Incorrect method", status=400)
        # return JSONResponse(Popen(args).read(), status=200)
    except Exception as e:
        return JSONResponse(e, status=400)


def check_dirs():
    print('Checking directories.')
    if os.path.exists(CONF_DIR):
        print('CONF_DIR.............................................OK')
    else:
        os.makedirs(CONF_DIR)
        print('CONF_DIR has been created............................OK')

    if os.path.exists(LOG_DIR):
        print('LOG_DIR..............................................OK')
    else:
        os.makedirs(LOG_DIR)
        print('LOG_DIR has been created.............................OK')


def check_config():
    print('Checking configuration files.')
    path = ''.join([CONF_DIR, 'ipf.conf'])
    if os.path.exists(path):
        print('ipf.conf.............................................OK')
    else:
        with open(path, 'a') as f:
            f.write('#filter configuration')
        print('ipf.conf has been created............................OK')

    path = ''.join([CONF_DIR, 'ipf6.conf'])
    if os.path.exists(path):
        print('ipf6.conf............................................OK')
    else:
        with open(path, 'a') as f:
            f.write('#ipf6 configuration')
        print('ipf6.conf has been created...........................OK')

    path = ''.join([CONF_DIR, 'ipnat.conf'])
    if os.path.exists(path):
        print('ipnat.conf...........................................OK')
    else:
        with open(path, 'a') as f:
            f.write('#NAT configuration')
        print('ipnat.conf has been created..........................OK')

    path = ''.join([CONF_DIR, 'ippool.conf'])
    if os.path.exists(path):
        print('ippool.conf..........................................OK')
    else:
        with open(path, 'a') as f:
            f.write('#ippool configuration\n\n{}'.format(CONF_WARNING))
        print('ippool.conf has been created.........................OK')

    print('Startup configuration done.\n')


def update_blacklist():
    url = 'http://myip.ms/files/blacklist/general/full_blacklist_database.zip'
    directory = '/tmp/'
    zip_file = ''.join([directory, 'full_blacklist_database.zip'])
    txt_file = ''.join([directory, 'full_blacklist_database.txt'])
    conf_file = ''.join([CONF_DIR, 'ippool.conf'])

    try:
        print('Downloading updates.')
        wget.download(url, zip_file)
    except Exception as e:
        return e

    try:
        with zipfile.ZipFile(zip_file, 'r') as f:
            f.extractall(directory)
        print('\nUnzip file...........................................OK')
    except Exception as e:
        return e

    try:
        with open(txt_file, 'r') as database:

            with open(conf_file, 'r') as ippool:
                other_pools = ''.join(ippool.readlines()).split(CONF_WARNING)[0]

            with open(conf_file, 'w') as ippool:
                ippool.write(other_pools+CONF_WARNING+'\n\n'+
                             'blacklist role = ipf type = tree number = 1\n{\n')
                for line in database.readlines()[15:]:
                    ippool.write(line.split()[0]+',\n')
                ippool.write('}')
        print('Blacklist update.....................................OK')
    except Exception as e:
        return e

    try:
        os.remove(zip_file)
        os.remove(txt_file)
    except Exception as e:
        return e

    '''try:
        Popen('ippool -F')
        Popen('ippoll -f {}'.format(conf_file))
    except Exception as e:
        return e
    '''


def system_start():
    check_dirs()
    check_config()
    # update_blacklist()
    schedule.every().day.do(update_blacklist)

    while True:
        schedule.run_pending()
        time.sleep(3600)


def system_exit():
    f = open(os.devnull, 'w')
    sys.stderr = f
    sys.exit()