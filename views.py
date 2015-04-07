from subprocess import Popen
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from eszone_ipf.settings import CONF_DIR, LOG_DIR
from api_ipf.models import ConfigFile, LogFile
from api_ipf.serializers import ConfigFileSerializer, LogFileSerializer
from api_ipf.helpers import *


@csrf_exempt
@api_view(['GET', 'POST'])
def config(request):

    if request.method == 'GET':
        conf_list = ConfigFile.objects.all()
        serializer = ConfigFileSerializer(conf_list, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        # empty files problem, unique titles
        serializer = ConfigFileSerializer(data=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse('File uploaded.', status=201)
        else:
            return JSONResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def config_detail(request, title):

    try:
        config = ConfigFile.objects.get(title=title)
        path = ''.join([CONF_DIR, title])
    except ConfigFile.DoesNotExist:
        return JSONResponse('Error: No such file (db).', status=404)

    if request.method == 'GET':
        try:
            return JSONResponse(file_content(file), status=200)
        except IOError:
            return JSONResponse('Error: No such file (disk).', status=404)

    elif request.method == 'PUT':
        serializer = ConfigFileSerializer(config, data=request.FILES)
        if serializer.is_valid():
            try:
                file_move(path, title)
                serializer.save()
                return JSONResponse('File modified.')
            except Exception as e:
                return HttpResponse(e)
        else:
            return JSONResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        try:
            config.delete()
            file_delete(path)
            return JSONResponse('File deleted.', status=204)
        except Exception as e:
            return HttpResponse(e)


@csrf_exempt
@api_view(['GET', 'POST'])
def log(request):

    if request.method == 'GET':
        log_list = LogFile.objects.all()
        serializer = LogFileSerializer(log_list, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        serializer = LogFileSerializer(data=request.DATA)

        if serializer.is_valid():
            #Popen('ipmon -aD {}'.format(''.join([LOG_DIR, request.data['title']])))
            serializer.save()
            return JSONResponse('Log created.', status=200)
        else:
            return JSONResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'DELETE'])
def log_detail(request, title):

    try:
        log = LogFile.objects.get(title=title)
        path = ''.join([LOG_DIR, title, '.log'])
    except LogFile.DoesNotExist:
        return JSONResponse('Error: No such file (db).', status=404)

    if request.method == 'GET':
        try:
            return JSONResponse(file_content(path), status=200)
        except IOError:
            return JSONResponse('Error: No such file (disk).', status=404)

    elif request.method == 'DELETE':
        try:
            #Popen('pkill ipmon')
            log.delete()
            file_delete(path)
            return JSONResponse('File deleted.', status=204)
        except Exception as e:
            return HttpResponse(e)

@csrf_exempt
@api_view(['GET'])
def other_commands(request, args):

    if request.method == 'GET':
        try:
            return JSONResponse(args)
            #return JSONResponse(Popen(arg).read())
        except Exception as e:
            return HttpResponse(e)