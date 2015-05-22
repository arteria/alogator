#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
import json
from os.path import getsize
from datetime import datetime

from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils import timezone

import requests

from alogator import __version__ as alogator_version

import logging
logger = logging.getLogger('alogator')

from alogator.models import LogFile

PASSES = 0
logFileObjects = LogFile.objects.all()


def getLogFileObjects():
    global logFileObjects
    logFileObjects = LogFile.objects.all()


def logWatcher():
    global PASSES
    if PASSES > 10:
        getLogFileObjects()
        PASSES = 0
    PASSES += 1

    for logFileObj in logFileObjects:
        analyzeFile(logFileObj)


def analyzeFile(logFileObj):
    logFilename = logFileObj.path
    lastSize = logFileObj.lastSize
    lastPosition = logFileObj.lastPosition
    lastModified = logFileObj.lastModified

    try:
        logfile = codecs.open(logFilename, 'r', 'utf-8')
    except Exception as e:
        logger.error("EX42: " + str(e))
        # TODO: set to mute
        return False

    thisSize = getsize(logFilename)

    if not lastSize:
        lastSize = thisSize

    fileStats = os.stat(logFilename)
    thisModified = datetime.fromtimestamp(fileStats.st_mtime)
    thisModified = timezone.make_aware(thisModified, timezone.get_default_timezone())

    if not lastModified:
        lastModified = thisModified

    if not lastPosition:
        lastPosition = 0
    thisPosition = lastPosition

    if thisModified != lastModified:  # file was modified
        for sensor in logFileObj.sensors.all():
            sensor.inactive = False
            sensor.save()
        if thisSize > lastSize:  # file got bigger
            # go from last position to end and search for Keywords
            logfile.seek(lastPosition)
            readTail(logfile, logFileObj)
            thisPosition = logfile.tell()

        elif thisSize < lastSize:
            logfile.seek(0)
            readTail(logfile, logFileObj)
            thisPosition = logfile.tell()
        else:
            pass
        logFileObj.lastSize = thisSize
        logFileObj.lastPosition = thisPosition
        logFileObj.lastModified = thisModified
        logFileObj.save()
    else:
        inactive = timezone.now() - thisModified
        inactive_secons = inactive.total_seconds()

        sensors = logFileObj.sensors.filter(inactivityThreshold__isnull=False).exclude(inactivityThreshold=0)
        for sensor in sensors:
            if inactive_secons > sensor.inactivityThreshold and not sensor.inactive:
                sensor.inactive = True
                sensor.save()
                if sensor.actor.active and not sensor.actor.mute:
                    sendNotification(sensor, "alogator inactivityThreshold reached", logFileObj.path)
                elif sensor.actor.active and sensor.actor.mute:
                    collectForMuted(sensor.actor, "alogator inactivityThreshold reached")

    logfile.close()


def sendNotification(sensor, line, path=""):
    if sensor.actor:
        if sensor.actor.email:
            targetEmail = sensor.actor.email
            content = render_to_string("alogator/email/pattern_found.txt", {
                'line': line,
                'path': path,
                'pattern': sensor.pattern
            })
            try:
                send_mail('Alogator: pattern found', content, 'debug@arteria.ch', [targetEmail], fail_silently=True)
            except Exception as ex:
                logger.error('sendNotification ' + str(ex))
            else:
                logger.debug('Found pattern, send Email to' + targetEmail)
        if sensor.actor.slackHook:
            slackHook = sensor.actor.slackHook
            slackChannel = getattr(sensor.actor, 'slackChannel', '')

            text = render_to_string("alogator/email/slack_message.txt", {
                'line': line,
                'path': path,
                'pattern': sensor.pattern
            })
            payload = {
                'text': text,
                'channel': slackChannel,
                'icon_emoji': ':bangbang:',
                'username': 'alogator',
            }
            r = requests.post(slackHook, data=json.dumps(payload))
            if r.ok:
                logger.debug('Slack notification: ' + slackChannel)
            else:
                logger.error('Slack notification failed. channel: ' + slackChannel)

        if sensor.actor.postHook:
            payload = {
                'line': line,
                'path': path,
                'sensor': sensor.pk,
                'inactivityThreshold': sensor.inactivityThreshold,
                'caseSensitive': sensor.caseSensitive,
                'actor': sensor.actor.pk,
                'log': sensor.logfile_set.get().pk,
                'version': alogator_version,
            }
            r = requests.post(sensor.actor.postHook, data=json.dumps(payload))
            if r.ok:
                logger.debug('Hock post ' + sensor.actor.postHook)
            else:
                logger.error('Hock post failed ' + sensor.actor.postHook)

    else:
        logger.error('Sensor ' + str(sensor) + ' has no actor.')


def findPattern(logfile, logFileObj, line):
    sensors = logFileObj.sensors.all()
    line = line.replace('\n', '')
    for sensor in sensors:
        n_line = line
        if not sensor.caseSensitive:
            sensor.pattern = sensor.pattern.lower()
            n_line = n_line.lower()
        if sensor.pattern and sensor.pattern in n_line:
            if sensor.actor.active and not sensor.actor.mute:
                sendNotification(sensor, line, logFileObj.path)
            elif sensor.actor.active and sensor.actor.mute:
                collectForMuted(sensor.actor, line)


def readTail(logfile, logFileObj):
    logger.debug('File was modified. Searching for pattern')
    while True:
        character = logfile.read(1)
        if character:
            lineChars = []
            lineChars.append(character)
            while True:
                character = logfile.read(1)
                if character:
                    lineChars.append(character)
                    if character == '\n':
                        line = ''.join(lineChars)
                        findPattern(logfile, logFileObj, line)
                        break
                    else:
                        pass
                else:  # reached end of file
                    break
        else:
            break


def collectForMuted(actor, line):
    s = "actor id: %s email: %s (actor muted)___%s" % (actor.id, actor.email, line)
    f = open(actor.getMutedFilename(), 'a')
    f.write(s)
    f.close()


# helper function for debugging
def writeToFile(text, path="/tmp/alogator-debug.log"):
    f = open(path, 'a')
    f.write(text + '\n')
    f.flush()


def getBasename(path):
    """returns filename for a given path e.g. "out.log" for "/tmp/alogator/out.log"
    """
    return os.path.basename(path)
