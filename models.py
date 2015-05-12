from django.db import models
from api_ipf.settings import CONF_DIR, LOG_DIR
import sh

class ConfigFile(models.Model):
    """
    Model that stores a serialized configuration of a IPFilter. Configuration
    file is defined by unique title, form, path where is stored, creation and
    modification time. Allowed forms are ipf, ipf6, ipnat and ippool.
    """
    title = models.CharField(max_length=100, primary_key=True)
    form = models.CharField(max_length=10, default='ipf')
    directory = models.FileField(upload_to=CONF_DIR, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_form(self):
        """
        Method that returns form of a configuration file for processes of
        activation and check configuration file at its upload.

        :return: file's form
        """
        return self.form


class LogFile(models.Model):
    """
    Model that stores a serialized log of a IPFilter log management. Log file
    is defined by unique title, path where is stored and creation time.
    """
    title = models.CharField(max_length=100, primary_key=True)
    directory = models.FileField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Method that overrides basic save method. Log is created in a specific
        location defined in LOG_CONF and logging is redirect to the log by
        command ipmon -aD.

        :return: path to the log
        """
        path = ''.join([LOG_DIR, self.title, '.log'])
        open(path, 'a').close()
        self.log = path
        sh.ipmon('-aD', path)
        super(LogFile, self).save(*args, **kwargs)
        return self.directory
