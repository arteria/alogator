#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template.loader import render_to_string
from django.core.mail import send_mail

import os
import codecs
from os.path import getsize
from datetime import datetime

import logging
logger = logging.getLogger('django')

from .models import LogFile

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
    except Exception, e:
        logger.error("EX42: "+ str(e))
        # TODO: set to mute
        return False

    thisSize = getsize(logFilename)

    if not lastSize:
        lastSize = thisSize

    fileStats = os.stat(logFilename)
    thisModified = datetime.fromtimestamp(fileStats.st_mtime)

    if not lastModified:
        lastModified = thisModified

    if not lastPosition:
        lastPosition = 0
    thisPosition = lastPosition

    if thisModified != lastModified:  # file was modified
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
        pass

    logfile.close()


def sendEmail(sensor, line, path=""):
    if sensor.actor:
        targetEmail = sensor.actor.email
        content = render_to_string("alogator/email/pattern_found.txt", {
                'line': line, 'path': path, 'pattern': sensor.pattern })
        send_mail('Alogator: pattern found', content, 'debug@arteria.ch', [targetEmail], fail_silently=True)
        logger.debug('Found pattern, send Email to' + targetEmail)
    else:
        logger.error('Sensor ' + str(sensor) + ' has no actor.')


def findPattern(logfile, logFileObj, line):
    sensors = logFileObj.sensors.all()
    line = line.replace('\n', '')
    for sensor in sensors:
        if not sensor.caseSensitive:
            sensor.pattern = sensor.pattern.lower()
            line = line.lower()
        if sensor.pattern in line:
            if sensor.actor.active and not sensor.actor.mute:
                sendEmail(sensor, line, logFileObj.path)
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
def writeToFile(text):
    f = open("/tmp/alogator-debug.log", 'a')
    f.write(text + '\n')
    f.flush()


def getBasename(path):
    """returns filename for a given path e.g. "out.log" for "/tmp/alogator/out.log"
    """
    return os.path.basename(path)
