import json

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Get JSON representing the less which needs compilation for the project'

    def handle(self, *args, **options):
        self.stdout.write(json.dumps(settings.LESS_COMPILATIONS))
