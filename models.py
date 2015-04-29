from django.db import models
from eszone_ipf.settings import CONF_DIR, BCK_DIR, LOG_DIR

class ConfigFile(models.Model):
    title = models.CharField(max_length=100, primary_key=True)
    type = models.CharField(max_length=10, default='ipf')
    directory = models.FileField(upload_to=CONF_DIR)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.type in ['ipf', 'nat', 'ippool']:
            super(ConfigFile, self).save(*args, **kwargs)

    def get_type(self):
        return self.type


class LogFile(models.Model):
    title = models.CharField(max_length=100, primary_key=True)
    directory = models.FileField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        path = ''.join([LOG_DIR, self.title, '.log'])
        open(path, 'a').close()
        self.log = path
        super(LogFile, self).save(*args, **kwargs)