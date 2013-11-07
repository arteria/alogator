from django.core.management.base import BaseCommand, CommandError
from alogator.logwatch import logWatcher

class Command(BaseCommand):

    def handle(self):
        logWatcher()