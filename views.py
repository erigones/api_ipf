from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view

from api_ipf.models import ConfigFile
from api_ipf.serializers import ConfigFileSerializer
from api_ipf.helpers import *


def test(request):
    return HttpResponse('Test completed.')

@csrf_exempt
@api_view(['GET', 'POST'])
def config(request):

    if request.method == 'GET':
        file_list = ConfigFile.objects.all()
        serializer = ConfigFileSerializer(file_list, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        #empty files problem, unique titles
        serializer = ConfigFileSerializer(data=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse('File uploaded.', status=201)
        else:
            return JSONResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def config_detail(request, title):

    try:
        config = ConfigFile.objects.get(title=title)
    except ConfigFile.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        try:
            return HttpResponse(get_content(title), status=200)
        except IOError:
            return HttpResponse('Error: No such file or directory.', status=404)

    elif request.method == 'PUT':
        serializer = ConfigFileSerializer(config, data=request.FILES)
        if serializer.is_valid():
            file_delete(str(request.FILES['title']))
            serializer.save()
            return HttpResponse('File modified.')
        else:
            return JSONResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        try:
            config.delete()
            file_delete(title)
            return HttpResponse('File deleted.', status=204)
        except Exception as e:
            return HttpResponse(e)

@csrf_exempt
@api_view(['GET'])
def ipfstat(request, arg):

    if request.method == 'GET':
        try:
            return HttpResponse(arg)
            #return Popen('ipfstat {}'.format(arg)).read()
        except Exception as e:
            return HttpResponse(e)

@csrf_exempt
@api_view(['GET'])
def ipnat(request, arg):

    if request.method == 'GET':
        try:
            return HttpResponse(arg)
            #return Popen('ipnat {}'.format(arg)).read()
        except Exception as e:
            return HttpResponse(e)

@csrf_exempt
@api_view(['GET', 'PUT'])
def firewall(request, arg):

    try:
        status = get_status()
    except Exception as e:
        return HttpResponse(e)

    if request.method == 'GET':
        try:
            return HttpResponse(status)
        except Exception as e:
            return HttpResponse(e)

    elif request.method == 'PUT':

        try:
            if arg == 'start':
                if status == 'disabled':
                    return HttpResponse(enable_firewall())
                elif status == 'online':
                    return HttpResponse('Firewall is already started.')
            elif arg == 'stop':
                if status == 'online':
                    return HttpResponse(disable_firewall())
                else:
                    return HttpResponse('Firewall is already stopped.')
            else:
                raise Exception('Error: Wrong argument.')
        except Exception as e:
            return HttpResponse(e)

