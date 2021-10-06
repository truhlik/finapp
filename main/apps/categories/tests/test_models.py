from django.test import TestCase

from ..models import Category


class CategoryModelTestCase(TestCase):
    fixtures = ['categories.json']

    def test_get_bank_account(self):
        c = Category.objects.get(slug='bank-accounts')
        self.assertEqual(c, Category.get_bank_account())

    def test_get_bond(self):
        c = Category.objects.get(slug='bonds')
        self.assertEqual(c, Category.get_bond())

    def test_get_building_saving(self):
        c = Category.objects.get(slug='building-savings')
        self.assertEqual(c, Category.get_building_saving())

    def test_get_commodity(self):
        c = Category.objects.get(slug='commodities')
        self.assertEqual(c, Category.get_commodity())

    def test_get_crypto(self):
        c = Category.objects.get(slug='cryptos')
        self.assertEqual(c, Category.get_crypto())

    def test_get_pension_saving(self):
        c = Category.objects.get(slug='pension-savings')
        self.assertEqual(c, Category.get_pension_saving())

    def test_get_saving_account(self):
        c = Category.objects.get(slug='saving-accounts')
        self.assertEqual(c, Category.get_saving_account())

    def test_get_share_etf(self):
        c = Category.objects.get(slug='share-etf')
        self.assertEqual(c, Category.get_share_etf())

    def test_get_stock(self):
        c = Category.objects.get(slug='stocks')
        self.assertEqual(c, Category.get_stock())

    def test_get_term_accounts(self):
        c = Category.objects.get(slug='term-accounts')
        self.assertEqual(c, Category.get_term_account())

    def test_get_property(self):
        c = Category.objects.get(slug='properties')
        self.assertEqual(c, Category.get_property())

    def test_get_category_dict(self):
        self.assertEqual(11, len(Category.get_category_dict()))
