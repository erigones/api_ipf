from django.db import models
from eszone_ipf.settings import CONF_DIR

class ConfigFile(models.Model):
    title = models.CharField(max_length=100, primary_key=True)
    logfile = models.FileField(upload_to=CONF_DIR)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    #https://gist.github.com/bryanchow/1195854 microsecond replacement