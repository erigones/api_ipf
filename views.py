from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view

from api_ipf.models import ConfigFile
from api_ipf.serializers import ConfigFileSerializer
from api_ipf.helpers import *

#from rest_framework.exceptions import APIException

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
            return JSONResponse('File uploaded.', status=201)
        else:
            return JSONResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def config_detail(request, title):

    try:
        config = ConfigFile.objects.get(title=title)
    except ConfigFile.DoesNotExist:
        return JSONResponse('Error: No such file (db).', status=404)

    if request.method == 'GET':
        try:
            return JSONResponse(get_content(title), status=200)
        except IOError:
            return JSONResponse('Error: No such file (disk).', status=404)

    elif request.method == 'PUT':
        serializer = ConfigFileSerializer(config, data=request.FILES)
        if serializer.is_valid():
            file_delete(str(request.FILES['title']))
            serializer.save()
            return JSONResponse('File modified.')
        else:
            return JSONResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        try:
            config.delete()
            file_delete(title)
            return JSONResponse('File deleted.', status=204)
        except Exception as e:
            return HttpResponse(e)

@csrf_exempt
@api_view(['GET'])
def firewall(request, arg):

    try:
        status = get_status()
    except Exception as e:
        return JSONResponse(e)

    if request.method == 'GET':

        try:
            if arg == 'start':
                if status == 'disabled':
                    return JSONResponse(change_state('enable'), status=200)
                elif status == 'online':
                    return JSONResponse('Firewall is already started.')
            elif arg == 'stop':
                if status == 'online':
                    raise MyException()
                    #return JSONResponse(change_state('disable'), status=200)
                else:
                    return JSONResponse('Firewall is already stopped.')
            elif not arg:
                return JSONResponse(status, status=200)
            else:
                raise Exception('Error: Wrong argument.')
        except Exception as e:
            return JSONResponse(e)

@csrf_exempt
@api_view(['GET', 'POST'])
def log(request):

    if request.method == 'GET':
        try:
            return JSONResponse(get_log(), status=200)
        except Exception as e:
            return HttpResponse(e)

    elif request.method == 'POST':
        try:
            return JSONResponse(modify_log(request.DATA['title']), status=200)
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