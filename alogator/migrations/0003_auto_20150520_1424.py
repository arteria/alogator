# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alogator', '0002_auto_20150520_1106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logsensor',
            old_name='inactivity_threshold',
            new_name='inactivityThreshold',
        ),
        migrations.AddField(
            model_name='logactor',
            name='postHook',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='logactor',
            name='slackChannel',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='logactor',
            name='slackHook',
            field=models.URLField(null=True, blank=True),
        ),
    ]
