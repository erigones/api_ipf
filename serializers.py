from rest_framework import serializers
from api_ipf.models import ConfigFile

class ConfigFileSerializer(serializers.ModelSerializer):

	class Meta:
		model = ConfigFile
		fields = ('logfile','title')
