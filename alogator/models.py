from django.db import models

from datetime import datetime 


class LogActor(models.Model):
    email = models.CharField(max_length=100, 
            blank=True, 
            null=True, 
            help_text='Alogator will send a messages to this email address.')
    active = models.BooleanField(default=True)
    mute = models.BooleanField(default=False, help_text="suppress for notification")
    
    def __unicode__(self):
        return 'email to: %s' % (self.email)

    def getMutedFilename(self):
        return "/tmp/alogator_actor_%s_muted" % self.id

    def save(self, *args, **kwargs):
        if not self.mute:
            from .logwatch import sendEmail
            try:
                f = open(self.getMutedFilename(), 'r')
                content = f.read()
            except:
                content = "Muted file " + self.getMutedFilename() + " does not exist."
            sendEmail(self, content, self.getMutedFilename())

            f = open(self.getMutedFilename(), 'a')
            f.flush()
        super(LogActor, self).save(*args, **kwargs)  # Call the "real" save() method.


class LogSensor(models.Model):
    pattern = models.CharField(max_length=100, blank=True, null=True)
    caseSensitive = models.BooleanField(default=False)
    actor = models.ForeignKey(LogActor)

    def __unicode__(self):
        return 'search for: %s' % (self.pattern)


class LogFile(models.Model):
    path = models.CharField(max_length=1000, blank=True, null=True)
    lastModified = models.DateTimeField(default=datetime.now, blank=True)
    lastPosition = models.IntegerField(default=0)
    lastSize = models.IntegerField(default=0)
    sensors = models.ManyToManyField(LogSensor, null=True, blank=True)

    def __unicode__(self):
        return self.path
 
