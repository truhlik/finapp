from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Seed data for categories'

    def handle(self, *args, **options):
        call_command('seed_currencies')
        call_command('seed_categories')
        call_command('seed_institutions')
        call_command('seed_products')
