from os import remove, makedirs, devnull
from os.path import exists
from shutil import copyfile
from subprocess import Popen
from datetime import datetime
from wget import download
from zipfile import ZipFile
from django.db import connection
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from api_ipf.settings import *
from api_ipf.serializers import ConfigFileSerializer
import sys
import sh
import schedule
import time


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
        remove(path)
        return JSONResponse('Config deleted.', status=204)
    except Exception as e:
        return JSONResponse(e, status=400)


def log_delete(log, path):
    try:
        sh.pkill('ipmon')
        log.delete()
        remove(path)
        return JSONResponse('Log deleted.', status=204)
    except Exception as e:
        return JSONResponse(e, status=400)


def config_addition(title, form):
    path = ''.join([CONF_DIR, title])

    try:
        if form not in ['ipf', 'ipnat', 'ippool', 'ipf6']:
            return JSONResponse('Incorrect type.', status=400)

        elif form in ['ipf', 'ipf6']:
            bck_file = sh.ipfstat('-io')
            if sh.ipf(f=path):
                sh.ipf('-Fa', f=bck_file)
                return JSONResponse('Incorrect ipf format.', status=400)
            return JSONResponse('Ipf Configuration added.', status=201)

        elif form == 'ipnat':
            bck_file = sh.ipnat('-l')
            if sh.ipnat(f=path):
                sh.ipnat('-FC', f=bck_file)
                return JSONResponse('Incorrect ipf format.', status=400)
            return JSONResponse('Nat configuration added.', status=201)

        elif form == 'ippool':
            bck_file = sh.ippool('-l')
            if sh.ippool(f=path):
                sh.ippool('-F')
                sh.ippool(f=bck_file)
                return JSONResponse('Incorrect ippool format.', status=400)
            return JSONResponse('Ippool configuration added.', status=201)

    except Exception as e:
        return JSONResponse(e, status=400)


def activate(form, path):

    try:
        if form in ['ipf', 'ipf6']:
            sh.ipf('-Fa', f=path)
        elif form == 'ipnat':
            sh.ipnat('-FC', f=path)
        elif form == 'ippool':
            sh.ippool('-F')
            sh.ippool(f=path)
            sh.svcadm('refresh', 'ipfilter')
        return JSONResponse('Configuration activated.', status=200)
    except Exception as e:
        return JSONResponse(e, status=400)


def realize_command(args):
    try:
        if args.split()[0] in ALLOWED_COMMANDS:
            return JSONResponse(Popen(args).read(), status=200)
        else:
            return JSONResponse("Incorrect method", status=400)
    except Exception as e:
        return JSONResponse(e, status=400)


def check_dirs():
    print('Checking directories.')
    if exists(CONF_DIR):
        print('CONF_DIR.............................................OK')
    else:
        makedirs(CONF_DIR)
        print('CONF_DIR has been created............................OK')

    if exists(LOG_DIR):
        print('LOG_DIR..............................................OK')
    else:
        makedirs(LOG_DIR)
        print('LOG_DIR has been created.............................OK')


def add_file_to_db(title, path):
    cursor = connection.cursor()
    date = datetime.now()
    cursor.execute(
            'INSERT INTO api_ipf_configfile VALUES ("{}","{}","{}","{}","{}")'
            .format(title+'.conf', title, path, date, date))


def check_config():

    print('Checking configuration files.')
    path = ''.join([CONF_DIR, 'ipf.conf'])
    if exists(path):
        print('ipf.conf.............................................OK')
    else:
        copyfile(''.join([CONF_DIR, '.ipf.bck']), path)
        add_file_to_db('ipf', path)
        print('ipf.conf has been created............................OK')

    path = ''.join([CONF_DIR, 'ipf6.conf'])
    if exists(path):
        print('ipf6.conf............................................OK')
    else:
        with open(path, 'a') as f:
            f.write('#ipf6 configuration')
        add_file_to_db('ipf6', path)
        print('ipf6.conf has been created...........................OK')

    path = ''.join([CONF_DIR, 'ipnat.conf'])
    if exists(path):
        print('ipnat.conf...........................................OK')
    else:
        with open(path, 'a') as f:
            f.write('#NAT configuration')
        add_file_to_db('ipnat', path)
        print('ipnat.conf has been created..........................OK')

    path = ''.join([CONF_DIR, 'ippool.conf'])
    if exists(path):
        print('ippool.conf..........................................OK')
    else:
        with open(path, 'a') as f:
            f.write('#ippool configuration\n\n{}'.format(CONF_WARNING))
        add_file_to_db('ippool', path)
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
        download(url, zip_file)
    except Exception as e:
        return e

    try:
        with ZipFile(zip_file, 'r') as f:
            f.extractall(directory)
        print('\nUnzip file...........................................OK')
    except Exception as e:
        return e

    try:
        with open(txt_file, 'r') as database:

            with open(conf_file, 'r') as ippool:
                other_pools = ''.join(ippool.readlines()).split(CONF_WARNING)[0]

            with open(conf_file, 'w') as ippool:
                ippool.write(other_pools + CONF_WARNING + '\n\n' +
                             'blacklist role = ipf type = tree number = 1\n{\n')
                for line in database.readlines()[15:]:
                    ippool.write(line.split()[0]+',\n')
                ippool.write('}')
        print('Blacklist update.....................................OK')
    except Exception as e:
        return e

    try:
        remove(zip_file)
        remove(txt_file)
    except Exception as e:
        return e

    try:
        sh.ippool('-F')
        sh.ippool(f=conf_file)
        sh.svcadm('refresh', 'ipfilter')
    except Exception as e:
        return e


def system_start():
    check_dirs()
    check_config()
    update_blacklist()
    schedule.every().day.do(update_blacklist)

    while True:
        schedule.run_pending()
        time.sleep(3600)


def system_exit():
    f = open(devnull, 'w')
    sys.stderr = f
    sys.exit()