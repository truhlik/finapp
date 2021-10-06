import datetime
from decimal import Decimal

from django.utils import timezone

from main.apps.portfolio.models import Portfolio
from main.apps.portfolio.utils import calculate_actual_portfolio_value
from main.apps.portfolio_values.models import PortfolioValue


def create_portfolio_value(portfolio: Portfolio) -> Decimal:
    value = calculate_actual_portfolio_value(portfolio)
    pv = PortfolioValue(
        portfolio=portfolio,
        date=timezone.now().date(),
        value=value,
    )
    pv.save()
    return value


def get_portfolio_value_for_date(portfolio: Portfolio, date: datetime.date) -> Decimal:
    return PortfolioValue.objects.get(portfolio=portfolio, date=date).value
