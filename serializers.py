from rest_framework import serializers

from service_ipf.api_ipf.models import ConfigFile, LogFile


class ConfigFileSerializer(serializers.ModelSerializer):
    """
    Model serializer that takes input from client's POST or PUT request and
    format it in the appropriate form that can be stored into a database.
    """
    class Meta:
        model = ConfigFile
        fields = ('directory','title', 'form',)


class AccessConfigFileSerializer(serializers.ModelSerializer):
    """
    Model serializer that servers and requested object from a database by
    a response to a client. Necessary for hiding path to file, which is shown
    in ConfigFileSerializer.
    """
    class Meta:
        model = ConfigFile
        fields = ('title', 'form', 'created', 'modified')


class LogFileSerializer(serializers.ModelSerializer):
    """
    Model serializer that takes input from a client's request and format it
    in the appropriate form that can be stored into database. Also serves
    an requested object from a database by a response to the client.
    """
    class Meta:
        model = LogFile
        fields = ('title',)