#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
from daemon import Daemon

# load settings to setup the daemon
try:
    from django.conf import settings
    gHasSettings = True
except ImportError:
    gHasSettings = False


class LogObserverDaemon(Daemon):
    def run(self):
        f = open("/tmp/logObserverDaemonLog.log", 'a')
        while True:
            try:
                """try:
                    # setup django + settings to work with ...
                    from django.core.management import setup_environ
                    import alogator.settings as gSettings
                    setup_environ(gSettings)
                    from django.conf import settings
                    hasSettings = True
                except ImportError:
                    hasSettings = False
                time.sleep(settings.OBSERVER_SLEEP_TIME)
                """
                time.sleep(10)
                
                from .logwatch import logWatcher
                logWatcher()
            except Exception, ex:
                f.write("EX35: %s\n" % (str(ex),))
                f.flush()


if __name__ == "__main__":
    try:
        pidfile = '/tmp/daemon-' + sys.argv[0].replace('py', 'pid').replace('./', '')
        print "Current pid file is", pidfile
        daemon = LogObserverDaemon(pidfile)
        if len(sys.argv) == 2 and gHasSettings is True:
            if 'start' == sys.argv[1]:
                print "Stating..."
                daemon.start()
            elif 'stop' == sys.argv[1]:
                print "Stoping..."
                daemon.stop()
            elif 'restart' == sys.argv[1]:
                print "Restating..."
                daemon.restart()
            elif 'status' == sys.argv[1]:
                daemon.status()
            else:
                print "Unknown command"
                sys.exit(2)
            sys.exit(0)
        elif gHasSettings is False:
            print "Error: No settings found - is the env activated?"
        else:
            print "Usage: %s start|stop|status|restart" % sys.argv[0]
        sys.exit(2)
    except Exception, ex:
        print ex
        sys.exit(3)
