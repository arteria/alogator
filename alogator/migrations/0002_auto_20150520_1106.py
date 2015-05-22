# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alogator', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logfile',
            name='inactivity_threshold',
        ),
        migrations.AddField(
            model_name='logsensor',
            name='inactivity_threshold',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
    ]
