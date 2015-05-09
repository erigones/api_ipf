from django.db import models
from subprocess import Popen
from api_ipf.settings import CONF_DIR, LOG_DIR

class ConfigFile(models.Model):
    title = models.CharField(max_length=100, primary_key=True)
    type = models.CharField(max_length=10, default='ipf')
    directory = models.FileField(upload_to=CONF_DIR, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_type(self):
        return self.type


class LogFile(models.Model):
    title = models.CharField(max_length=100, primary_key=True)
    directory = models.FileField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        path = ''.join([LOG_DIR, self.title, '.log'])
        open(path, 'a').close()
        self.log = path
        Popen('ipmon -aD {}'.format(path))
        super(LogFile, self).save(*args, **kwargs)