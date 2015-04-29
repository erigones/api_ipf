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
            response = activate_config(request.FILES)
            if response.status_code != 406:
                serializer.save()
            return response
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
        return file_content(path)

    elif request.method == 'PUT':
        request.FILES['type'] = config.get_type()
        serializer = ConfigFileSerializer(config, data=request.FILES)
        if serializer.is_valid():
            response = activate_config(request.FILES)
            if response.status_code != 406:
                serializer.save()
            return response
        else:
            return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        return file_delete(config, path)


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
        return file_content(path)

    elif request.method == 'DELETE':
        return file_delete(log, path)

@csrf_exempt
@api_view(['GET'])
def other_commands(request, args):

    if request.method == 'GET':
        return realize_command(args)