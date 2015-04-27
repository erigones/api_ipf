from subprocess import Popen
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from api_ipf.serializers import *
from api_ipf.helpers import *


@csrf_exempt
@api_view(['GET', 'POST'])
def config(request):

    if request.method == 'GET':
        conf_list = ConfigFile.objects.all()
        serializer = ModifiedSerializer(conf_list, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        serializer = ConfigFileSerializer(data=request.FILES)
        if serializer.is_valid():
            serializer.save()
            path = ''.join([CONF_DIR, request.FILES['title']])
            if request.FILES['activate'] in ['Y', 'y', 'Yes', 'yes']:
                activate_config(path, request.FILES['type'])
            elif request.FILE['type'] == 'ippool':
                add_pool(path)
            return JSONResponse('Configuration created.', status=201)
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
            return JSONResponse(file_content(path), status=200)
        except IOError:
            return JSONResponse('Error: No such file (disk).', status=404)

    elif request.method == 'PUT':
        request.FILES['type'] = config.get_type()
        serializer = ConfigFileSerializer(config, data=request.FILES)
        if serializer.is_valid():
            file_delete(path)
            serializer.save()
            if request.FILES['activate'] in ['Y', 'y', 'Yes', 'yes']:
                activate_config(path, request.FILES['type'])
            return JSONResponse('Configuration modified.')
        else:
            return JSONResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        try:
            config.delete()
            file_delete(path)
            return JSONResponse('Configuration deleted.', status=204)
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
            return JSONResponse('Log deleted.', status=204)
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