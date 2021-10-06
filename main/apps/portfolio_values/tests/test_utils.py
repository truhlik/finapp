from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from .. import utils
from ...categories.models import Category
from ...portfolio.utils import get_portfolio_value


class PortfolioValuesUtilsTestCase(TestCase):
    fixtures = ['currencies.json', 'categories.json']

    def test_get_portfolio_value_for_date(self):
        p1 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_stock(), value=2)
        yesterday = timezone.now() - timezone.timedelta(days=1)
        baker.make('portfolio_values.PortfolioValue', portfolio=p1, value=7788, date=timezone.now().date())
        baker.make('portfolio_values.PortfolioValue', portfolio=p1, value=5544, date=yesterday)
        self.assertEqual(5544, utils.get_portfolio_value_for_date(p1, yesterday))

    def test_create_portfolio_value(self):
        product = baker.make_recipe('main.apps.products.product', value=4321, category=Category.get_commodity())
        p1 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_commodity(), product=product, units=1000)
        utils.create_portfolio_value(portfolio=p1)
        qs = p1.portfolio_values.all()
        self.assertEqual(1, len(qs))
        self.assertEqual(4321 * 1000, qs[0].value)
