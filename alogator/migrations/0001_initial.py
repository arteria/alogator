# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogActor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(help_text=b'Alogator will send a messages to this email address.', max_length=100, null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('mute', models.BooleanField(default=False, help_text=b'suppress for notification')),
            ],
        ),
        migrations.CreateModel(
            name='LogFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(max_length=1000, null=True, blank=True)),
                ('lastModified', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('lastPosition', models.IntegerField(default=0)),
                ('lastSize', models.IntegerField(default=0)),
                ('inactivity_threshold', models.IntegerField(default=0, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='LogSensor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pattern', models.CharField(max_length=100, null=True, blank=True)),
                ('caseSensitive', models.BooleanField(default=False)),
                ('actor', models.ForeignKey(to='alogator.LogActor')),
            ],
        ),
        migrations.AddField(
            model_name='logfile',
            name='sensors',
            field=models.ManyToManyField(to='alogator.LogSensor', null=True, blank=True),
        ),
    ]
