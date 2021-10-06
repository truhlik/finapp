from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Seed data for currencies'

    def handle(self, *args, **options):
        call_command('loaddata', 'currencies.json')
