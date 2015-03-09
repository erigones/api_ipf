from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view

from api_ipf.models import ConfigFile
from api_ipf.serializers import ConfigFileSerializer
from api_ipf.helpers import JSONResponse, get_content, file_delete
from eszone_ipf.settings import CONF_DIR

def test(request):
    return HttpResponse("Test completed.")

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
            return e