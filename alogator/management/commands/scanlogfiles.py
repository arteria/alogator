from django.core.management.base import BaseCommand, CommandError
from alogator.logwatch import logWatcher

class Command(BaseCommand):
    args = ''
    help = 'Scan logfiles for patterns.'

    def handle(self, *args, **options):
        self.stdout.write('Scanning logfiles...')
        logWatcher()
        self.stdout.write(' done. Good bye.')
            
 
        