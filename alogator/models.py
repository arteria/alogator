from django.db import models
from django.core.mail import send_mail

from django.utils import timezone


class LogActor(models.Model):
    email = models.CharField(max_length=100,
            blank=True,
            null=True,
            help_text='Alogator will send a messages to this email address.')
    active = models.BooleanField(default=True)
    mute = models.BooleanField(default=False, help_text="suppress for notification")

    slackHook = models.URLField(null=True, blank=True)
    slackChannel = models.CharField(max_length=50, null=True, blank=True)

    postHook = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return 'email to: %s' % (self.email)

    def getMutedFilename(self):
        return "/tmp/alogator_actor_%s_muted" % self.id

    def save(self, *args, **kwargs):
        if self.__class__.objects.get(pk=self.pk).mute and not self.mute:
            try:
                f = open(self.getMutedFilename(), 'r')
                content = f.read()
            except:
                content = "Muted file " + self.getMutedFilename() + " does not exist."
            send_mail(
                'ALOGATOR: Muged logs for: %s' % self.getMutedFilename(),
                content,
                'debug@arteria.ch',
                [self.email],
                fail_silently=True
            )

            f = open(self.getMutedFilename(), 'a')
            f.flush()
        super(LogActor, self).save(*args, **kwargs)  # Call the "real" save() method.


class LogSensor(models.Model):
    pattern = models.CharField(max_length=100, blank=True, null=True)
    caseSensitive = models.BooleanField(default=False)
    actor = models.ForeignKey(LogActor)

    inactivityThreshold = models.IntegerField(default=0, null=True, blank=True)
    inactive = models.BooleanField(default=False)

    def __unicode__(self):
        return 'search for: %s' % (self.pattern)


class LogFile(models.Model):
    path = models.CharField(max_length=1000, blank=True, null=True)
    lastModified = models.DateTimeField(default=timezone.now, blank=True)
    lastPosition = models.IntegerField(default=0)
    lastSize = models.IntegerField(default=0)
    sensors = models.ManyToManyField(LogSensor, blank=True)

    def __unicode__(self):
        return self.path
