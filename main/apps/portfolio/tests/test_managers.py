from decimal import Decimal

from django.test import TestCase
from model_bakery import baker

from ..models import Portfolio, BankAccount, Bond, SavingAccount, TermAccount, BuildingSaving
from ..models.commodity import Commodity
from ..models.crypto import Crypto
from ..models.pension_saving import PensionSaving
from ..models.share_etf import ShareEtf
from ..models.stock import Stock
from ...categories.models import Category
from ...currencies.models import Currency


class PortfolioQuerySetTestCase(TestCase):
    fixtures = ['categories.json', 'currencies.json']

    def test_active(self):
        i1 = baker.make(Portfolio, active=True, value=1)
        i2 = baker.make(Portfolio, active=False, value=1)
        qs = Portfolio.objects.active()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])

    def for_user(self):
        user = baker.make('users.User')
        i1 = baker.make(Portfolio, owner=user, value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = Portfolio.objects.for_user(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])

    def test_bank_accounts(self):
        i1 = baker.make(Portfolio, category=Category.get_bank_account(), value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = Portfolio.objects.bank_accounts()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])

    def test_bonds(self):
        i1 = baker.make(Portfolio, category=Category.get_bond(), value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = Portfolio.objects.bonds()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])

    def test_building_savings(self):
        i1 = baker.make(Portfolio, category=Category.get_building_saving(), value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = Portfolio.objects.building_savings()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])

    def test_commodities(self):
        i1 = baker.make(Portfolio, category=Category.get_commodity(), value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = Portfolio.objects.commodities()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])

    def test_cryptos(self):
        i1 = baker.make(Portfolio, category=Category.get_crypto(), value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = Portfolio.objects.cryptos()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])

    def test_pension_savings(self):
        i1 = baker.make(Portfolio, category=Category.get_pension_saving(), value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = Portfolio.objects.pension_savings()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])

    def test_saving_accounts(self):
        i1 = baker.make(Portfolio, category=Category.get_saving_account(), value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = Portfolio.objects.saving_accounts()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])

    def test_share_etfs(self):
        i1 = baker.make(Portfolio, category=Category.get_share_etf(), value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = Portfolio.objects.share_etfs()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])

    def test_stocks(self):
        i1 = baker.make(Portfolio, category=Category.get_stock(), value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = Portfolio.objects.stocks()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])

    def test_term_accounts(self):
        i1 = baker.make(Portfolio, category=Category.get_term_account(), value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = Portfolio.objects.term_accounts()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])

    def test_properties(self):
        i1 = baker.make(Portfolio, category=Category.get_property(), value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = Portfolio.objects.properties()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])

    def test_group_by_category(self):
        i1 = baker.make(Portfolio, category=Category.get_property(), value=1, current_eval=10, currency=Currency.get_czk())
        i2 = baker.make(Portfolio, category=Category.get_property(), value=2, current_eval=20, currency=Currency.get_czk())
        i3 = baker.make(Portfolio, category=Category.get_bank_account(), value=5, current_eval=5, currency=Currency.get_czk())
        qs = Portfolio.objects.group_by_category()
        exp_data = [
            {
                'category': 'bank-accounts',
                 'name': 'Běžné účty',
                 'current_eval': 5,
                 'ytd_eval': None,
                 'avg_eval': None,
                 'total_eval': None,
                 'weight_eval': None,
                 'currency_code': 'CZK',
                 'currency_name': 'Kč',
                 'value': 5
             },
            {
                'category': 'properties',
                'name': 'Nemovitosti',
                'current_eval': Decimal('16.67'),
                'ytd_eval': None,
                'avg_eval': None,
                'total_eval': None,
                'weight_eval': None,
                'currency_code': 'CZK',
                'currency_name': 'Kč',
                'value': 3,
            }
        ]
        self.assertEqual(2, len(qs))
        self.assertEqual(exp_data, list(qs))

    def test_group_by_category_zero(self):
        i3 = baker.make(Portfolio, category=Category.get_bank_account(), value=Decimal(0), current_eval=5, currency=Currency.get_czk())
        qs = Portfolio.objects.group_by_category()
        exp_data = [
            {
                'category': 'bank-accounts',
                 'name': 'Běžné účty',
                 'current_eval': 5,
                 'ytd_eval': None,
                 'avg_eval': None,
                 'total_eval': None,
                 'weight_eval': None,
                 'currency_code': 'CZK',
                 'currency_name': 'Kč',
                 'value': 0.0
             },
        ]
        self.assertEqual(exp_data, list(qs))

    def test_group_by_portfolio(self):
        i1 = baker.make(Portfolio, name='test', category=Category.get_property(), value=1, current_eval=10, currency=Currency.get_czk())
        i3 = baker.make(Portfolio, name='test1', category=Category.get_bank_account(), value=5, current_eval=5, currency=Currency.get_czk())
        qs = Portfolio.objects.group_by_portfolio()
        exp_data = [
            {
                'portfolio_id': i3.id,
                'category': 'bank-accounts',
                'name': 'test1',
                'current_eval': 5,
                'ytd_eval': None,
                'avg_eval': None,
                'total_eval': None,
                'weight_eval': None,
                'currency_code': 'CZK',
                'currency_name': 'Kč',
                'value': 5
            },
            {
                'portfolio_id': i1.id,
                'category': 'properties',
                'name': 'test',
                'current_eval': 10,
                'ytd_eval': None,
                'avg_eval': None,
                'total_eval': None,
                'weight_eval': None,
                'currency_code': 'CZK',
                'currency_name': 'Kč',
                'value': 1,
            }
        ]
        self.assertEqual(exp_data, list(qs))

    def test_group_by_portfolio_with_zero_values(self):
        i3 = baker.make(Portfolio, category=Category.get_bank_account(), value=Decimal(0), current_eval=5, currency=Currency.get_czk(), name='test1')
        qs = Portfolio.objects.group_by_portfolio()
        exp_data = [
            {
                'portfolio_id': i3.id,
                'category': 'bank-accounts',
                'name': 'test1',
                'current_eval': 5,
                'ytd_eval': None,
                'avg_eval': None,
                'total_eval': None,
                'weight_eval': None,
                'currency_code': 'CZK',
                'currency_name': 'Kč',
                'value': 0.0
            },
        ]
        self.assertEqual(exp_data, list(qs))


class BankAccountsManagerTestCase(TestCase):
    fixtures = ['categories.json']

    def test_get_queryset(self):
        i1 = baker.make(BankAccount, category=Category.get_bank_account(), value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = BankAccount.objects.all()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])


class BondsManagerTestCase(TestCase):
    fixtures = ['categories.json']

    def test_get_queryset(self):
        i1 = baker.make(Bond, category=Category.get_bond(), value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = Bond.objects.all()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])


class SavingAccountsManagerTestCase(TestCase):
    fixtures = ['categories.json']

    def test_get_queryset(self):
        i1 = baker.make(SavingAccount, value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = SavingAccount.objects.all()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])


class TermAccountsManagerTestCase(TestCase):
    fixtures = ['categories.json']

    def test_get_queryset(self):
        i1 = baker.make(TermAccount, value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = TermAccount.objects.all()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])


class BuildingSavingsManagerTestCase(TestCase):
    fixtures = ['categories.json']

    def test_get_queryset(self):
        i1 = baker.make(BuildingSaving, value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = BuildingSaving.objects.all()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])


class PensionSavingsManagerTestCase(TestCase):
    fixtures = ['categories.json']

    def test_get_queryset(self):
        i1 = baker.make(PensionSaving, value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = PensionSaving.objects.all()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])


class StocksManagerTestCase(TestCase):
    fixtures = ['categories.json']

    def test_get_queryset(self):
        i1 = baker.make(Stock, value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = Stock.objects.all()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])


class CryptosManagerTestCase(TestCase):
    fixtures = ['categories.json']

    def test_get_queryset(self):
        i1 = baker.make(Crypto, value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = Crypto.objects.all()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])


class CommoditiesManagerTestCase(TestCase):
    fixtures = ['categories.json']

    def test_get_queryset(self):
        i1 = baker.make(Commodity, value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = Commodity.objects.all()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])


class ShareEtfManagerTestCase(TestCase):
    fixtures = ['categories.json']

    def test_get_queryset(self):
        i1 = baker.make(ShareEtf, value=1)
        i2 = baker.make(Portfolio, value=1)
        qs = ShareEtf.objects.all()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])
