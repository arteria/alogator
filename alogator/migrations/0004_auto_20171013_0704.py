# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('alogator', '0003_auto_20150520_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='logsensor',
            name='inactive',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='logfile',
            name='lastModified',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='logfile',
            name='sensors',
            field=models.ManyToManyField(blank=True, to='alogator.LogSensor'),
        ),
        migrations.AlterField(
            model_name='logsensor',
            name='inactivityThreshold',
            field=models.IntegerField(blank=True, help_text=b'Inactivity threshold in seconds.', default=0, null=True),
        ),
    ]
