import datetime
from decimal import Decimal

from main.apps.portfolio.models import Portfolio
from main.apps.products.models import Product


def create_initial_value_for_portfolio(portfolio: Portfolio):
    from main.apps.portfolio_values.utils import create_portfolio_value
    value = create_portfolio_value(portfolio)
    set_portfolio_value(portfolio, value)


def calculate_actual_portfolio_value(portfolio: Portfolio) -> Decimal:
    return get_value_for_portfolio(portfolio.product, portfolio.units)


def get_portfolio_value(portfolio: Portfolio, date: datetime.date = None) -> Decimal:
    if date is None or date == datetime.date.today():
        return portfolio.value

    from main.apps.portfolio_values.utils import get_portfolio_value_for_date
    return get_portfolio_value_for_date(portfolio, date)


def set_portfolio_value(portfolio, value: Decimal, save=True) -> Portfolio:
    portfolio.value = value
    if save:
        portfolio.save(update_fields=['value'])
    return portfolio


def get_value_for_portfolio(product: Product, units: Decimal) -> Decimal:
    return product.value * units

