from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from service_ipf.api_ipf.serializers import *
from service_ipf.api_ipf.helpers import *


@csrf_exempt
@api_view(['GET', 'POST'])
def config(request):
    """
    An API view function that processes with a not specified file.

    In case of GET request returns list of all configuration files.
    In case of POST request takes data from request, serialize them, checks
    their correctness and stores them into a database.

    :param request: client's request
    :return: JSON response
    """
    if request.method == 'GET':
        conf_list = ConfigFile.objects.all()
        serializer = AccessConfigFileSerializer(conf_list, many=True)
        return JSONResponse(serializer.data, status=200)

    elif request.method == 'POST':
        serializer = ConfigFileSerializer(data=request.FILES)
        if serializer.is_valid():
            response = config_addition(str(request.FILES['title']),
                                       str(request.FILES['form']))
            if response.status_code == 201:
                serializer.save()
            return response
        else:
            return JSONResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def config_detail(request, title):
    """
    An API view function that processes request with a specified file.

    In case of GET request returns configuration file's content.
    In case of PUT request get itself form and data from request,
    serialize them, checks their correctness and stores them into a database.
    In case of DELETE request delete configuration file from a disk and object
    from a database.

    :param request: client's request
    :param title: a unique configuration file's title
    :return: JSON response
    """
    try:
        config = ConfigFile.objects.get(title=title)
        path = ''.join([CONF_DIR, title])
    except ConfigFile.DoesNotExist:
        return JSONResponse('Error: No such file (db).', status=404)

    if request.method == 'GET':
        return file_content(path)

    elif request.method == 'PUT':
        request.FILES['form'] = config.get_form()
        serializer = ConfigFileSerializer(config, data=request.FILES)
        if serializer.is_valid():
            response = config_addition(str(request.FILES['title']),
                                       str(request.FILES['form']))
            if response.status_code == 201:
                serializer.save()
            return response
        else:
            return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        return config_delete(config, path)


@csrf_exempt
@api_view(['GET'])
def config_activate(request, title):
    """
    An API view function that processes activation of configuration file.

    :param request: client's request
    :param title: a unique configuration file's title
    :return: JSON response
    """
    if request.method == 'GET':
        try:
            config = ConfigFile.objects.get(title=title)
            path = ''.join([CONF_DIR, title])
            return activate(config, path)
        except ConfigFile.DoesNotExist:
            return JSONResponse('Error: No such file (db).', status=404)


@csrf_exempt
@api_view(['GET', 'POST'])
def log(request):
    """
    An API view function that processes with a not specified log.

    In case of GET request returns list of all logs.
    In case of POST request takes data from request, serialize them, checks
    their validness and stores them into a database. Afterwards the function
    starts logging mechanism with a redirection of ipmon output to the log.

    :param request: client's request
    :return: JSON response
    """
    if request.method == 'GET':
        log_list = LogFile.objects.all()
        serializer = LogFileSerializer(log_list, many=True)
        return JSONResponse(serializer.data, status=200)

    elif request.method == 'POST':
        serializer = LogFileSerializer(data=request.DATA)
        if serializer.is_valid():
            path = serializer.save()
            sh.ipmon('-Fa', f=path)
            return JSONResponse('Log created.', status=200)
        else:
            return JSONResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'DELETE'])
def log_detail(request, title):
    """
    An API view function that processes request with a specified log.

    In case of GET request returns log's content.
    In case of DELETE request delete log from a disk and object from a database.

    :param request: client's request
    :param title: a unique log's title
    :return: JSON response
    """
    try:
        log = LogFile.objects.get(title=title)
        path = ''.join([LOG_DIR, title, '.log'])
    except LogFile.DoesNotExist:
        return JSONResponse('Error: No such file (db).', status=404)

    if request.method == 'GET':
        return file_content(path)

    elif request.method == 'DELETE':
        return log_delete(log, path)


@csrf_exempt
@api_view(['GET'])
def blacklist(request):
    """
    An API view function that updates IP blacklist on client's request.

    :param request: client's request
    :return: JSON response
    """
    if request.method == 'GET':
        response = update_blacklist()
        if response:
            return JSONResponse(response, status=400)
        return JSONResponse('Blacklist updated.', status=200)


@csrf_exempt
@api_view(['GET'])
def ipf(request, args):
    """
    An API view function that takes arguments from request and tries execute
    them with an ipf command.

    In case the execution was done returned is affirmative response 200 OK.
    In case an error occurs returned is negative response 400 BAD_REQUEST.

    :param request: client's request
    :param args: ipf arguments
    :return: JSON response
    """
    if request.method == 'GET':
        try:
            return JSONResponse(sh.ipf('","'.join(['"', args.split(), '"'])),
                                status=200)
        except sh.ErrorReturnCode_2 as e:
            return JSONResponse(e, status=400)


@csrf_exempt
@api_view(['GET'])
def ipnat(request, args):
    """
    An API view function that takes arguments from request and tries execute
    them with an ipnat command.

    In case the execution was done returned is affirmative response 200 OK.
    In case an error occurs returned is negative response 400 BAD_REQUEST.

    :param request: client's request
    :param args: ipnat arguments
    :return: JSON response
    """
    if request.method == 'GET':
        try:
            return JSONResponse(sh.ipnat('","'.join(['"', args.split(), '"'])),
                                status=200)
        except sh.ErrorReturnCode_2 as e:
            return JSONResponse(e, status=400)


@csrf_exempt
@api_view(['GET'])
def ippool(request, args):
    """
    An API view function that takes arguments from request and tries execute
    them with an ippool command.

    In case the execution was done returned is affirmative response 200 OK.
    In case an error occurs returned is negative response 400 BAD_REQUEST.

    :param request: client's request
    :param args: ippool arguments
    :return: JSON response
    """
    if request.method == 'GET':
        try:
            return JSONResponse(sh.ippool('","'.join(['"', args.split(), '"'])),
                                status=200)
        except sh.ErrorReturnCode_2 as e:
            return JSONResponse(e, status=400)


@csrf_exempt
@api_view(['GET'])
def ipfstat(request, args):
    """
    An API view function that takes arguments from request and tries execute
    them with an ipfstat command.

    In case the execution was done returned is affirmative response 200 OK.
    In case an error occurs returned is negative response 400 BAD_REQUEST.

    :param request: client's request
    :param args: ipfstat arguments
    :return: JSON response
    """
    if request.method == 'GET':
        try:
            return JSONResponse(sh.ipfstat(
                '","'.join(['"', args.split(), '"'])), status=200)
        except sh.ErrorReturnCode_2 as e:
            return JSONResponse(e, status=400)


@csrf_exempt
@api_view(['GET'])
def ipmon(request, args):
    """
    An API view function that takes arguments from request and tries execute
    them with an ipmon command.

    In case the execution was done returned is affirmative response 200 OK.
    In case an error occurs returned is negative response 400 BAD_REQUEST.

    :param request: client's request
    :param args: ipmon arguments
    :return: JSON response
    """
    if request.method == 'GET':
        try:
            return JSONResponse(sh.ipmon('","'.join(['"', args.split(), '"'])),
                                status=200)
        except sh.ErrorReturnCode_2 as e:
            return JSONResponse(e, status=400)


@csrf_exempt
@api_view(['GET'])
def svcadm(request, args):
    """
    An API view function that takes arguments from request and tries execute
    them with a svcadm command.

    In case the execution was done returned is affirmative response 200 OK.
    In case an error occurs returned is negative response 400 BAD_REQUEST.

    :param request: client's request
    :param args: svcadm arguments
    :return: JSON response
    """
    if request.method == 'GET':
        try:
            return JSONResponse(sh.svcadm('","'.join(['"', args.split(), '"'])),
                                status=200)
        except sh.ErrorReturnCode_2 as e:
            return JSONResponse(e, status=400)


@csrf_exempt
@api_view(['GET'])
def state(request):
    """
    An API view function that returns current IPFilter's state.

    In case the execution was done returned is affirmative response 200 OK.
    In case an error occurs returned is negative response 400 BAD_REQUEST.

    :param request: client's request
    :return: JSON response
    """
    if request.method == 'GET':
        try:
            return JSONResponse(
                sh.cut(sh.tail(sh.svcs('ipfilter'), n=1), d=' ', f=1),
                status=200)
        except sh.ErrorReturnCode_2 as e:
            return JSONResponse(e, status=400)