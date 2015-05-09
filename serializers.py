from rest_framework import serializers
from api_ipf.models import ConfigFile, LogFile

class ConfigFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConfigFile
        fields = ('directory','title', 'type',)


class AccessConfigFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConfigFile
        fields = ('title', 'type', 'created', 'modified')


class LogFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = LogFile
        fields = ('title',)