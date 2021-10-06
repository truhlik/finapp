from django.core.management.base import BaseCommand

from main.apps.products.utils import seed_from_csv


class Command(BaseCommand):
    help = 'Seed data for products'

    def handle(self, *args, **options):
        seed_from_csv()
