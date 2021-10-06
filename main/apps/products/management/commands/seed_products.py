from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Seed data for products'

    def handle(self, *args, **options):
        call_command('loaddata', 'products.json')
