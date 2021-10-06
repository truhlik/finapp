import math
import random
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from main.apps.portfolio.models import Portfolio
from main.apps.portfolio_values.models import PortfolioValue


class Command(BaseCommand):
    help = 'Seed test data for graphs'

    def add_arguments(self, parser):
        parser.add_argument('--portfolio_id', type=int, required=True)
        parser.add_argument('--count', type=int, required=True)
        parser.add_argument('--clean', action='store_true')

    def handle(self, *args, **options):
        portfolio_id = options['portfolio_id']
        try:
            portfolio = Portfolio.objects.get(id=portfolio_id)
        except Portfolio.DoesNotExist:
            raise CommandError('Portfolio "%s" does not exist' % portfolio_id)

        portfolio_orig_value = portfolio.current_eval

        count = options['count']
        if count < 0:
            raise CommandError('Count must be greater then 0')

        clean = options['clean']
        if clean:
            PortfolioValue.objects.filter(portfolio=portfolio).delete()

        start_date = timezone.now() - timezone.timedelta(days=count)

        value = Decimal(0)
        for i in range(0, count):
            value = Decimal(2000 + (math.sin(i) * 1000) * random.random())

            PortfolioValue.objects.update_or_create(
                portfolio=portfolio,
                date=start_date + timezone.timedelta(days=i),
                defaults={"value": value, }
            )
        portfolio.value = value
        portfolio.current_eval = ((value - portfolio_orig_value) / portfolio_orig_value) * 100
        portfolio.save()

