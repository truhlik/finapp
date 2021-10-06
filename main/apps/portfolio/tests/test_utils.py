from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from ..models import Portfolio
from .. import utils
from ...categories.models import Category
from ...currencies.models import Currency


class PortfolioUtilsTestCase(TestCase):
    fixtures = ['currencies.json', 'categories.json']

    def test_calculate_actual_portfolio_value_saving_account(self):
        product = baker.make_recipe('main.apps.products.product', value=1, category=Category.get_saving_account())
        p1 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_saving_account(), product=product, units=1000)
        self.assertEqual(1000, utils.calculate_actual_portfolio_value(p1))

    def test_calculate_actual_portfolio_value_stock(self):
        product = baker.make_recipe('main.apps.products.product', value=4321, category=Category.get_stock())
        p1 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_stock(), product=product, units=1000)
        self.assertEqual(4321 * 1000, utils.calculate_actual_portfolio_value(p1))

    def test_set_portfolio_value_without_save(self):
        p1 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_stock(), value=2)
        utils.set_portfolio_value(p1, 1000, save=False)
        self.assertEqual(1000, p1.value)
        p1.refresh_from_db()
        self.assertEqual(2, p1.value)

    def test_set_portfolio_value_with_save(self):
        p1 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_stock(), value=2)
        utils.set_portfolio_value(p1, 1000)
        self.assertEqual(1000, p1.value)
        p1.refresh_from_db()
        self.assertEqual(1000, p1.value)

    def test_get_portfolio_value(self):
        p1 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_stock(), value=2)
        yesterday = timezone.now() - timezone.timedelta(days=1)
        baker.make('portfolio_values.PortfolioValue', portfolio=p1, value=7788, date=timezone.now().date())
        baker.make('portfolio_values.PortfolioValue', portfolio=p1, value=5544, date=yesterday)
        self.assertEqual(2, utils.get_portfolio_value(p1))

    def test_get_portfolio_value_for_date(self):
        p1 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_stock(), value=2)
        yesterday = timezone.now() - timezone.timedelta(days=1)
        baker.make('portfolio_values.PortfolioValue', portfolio=p1, value=7788, date=timezone.now().date())
        baker.make('portfolio_values.PortfolioValue', portfolio=p1, value=5544, date=yesterday)
        self.assertEqual(5544, utils.get_portfolio_value(p1, yesterday))
