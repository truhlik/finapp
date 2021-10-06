from django.core.exceptions import ValidationError
from django.test import TestCase
from model_bakery import baker

from ..models import Portfolio
from ...categories.models import Category
from ...currencies.models import Currency


class PortfolioModelTestCase(TestCase):
    fixtures = ['currencies.json', 'categories.json']

    def test_clean_category_institution_fail(self):
        category = baker.make('categories.Category')
        institution = baker.make('institutions.Institution')
        p1 = baker.make_recipe('main.apps.portfolio.portfolio', category=category, institution=institution)
        with self.assertRaises(ValidationError):
            p1.clean()

    def test_clean_category_institution_success(self):
        category = baker.make('categories.Category')
        institution = baker.make('institutions.Institution')
        institution.categories.set([category])
        product = baker.make('products.Product', category=category, currencies=[Currency.get_czk()])
        product.institutions.add(institution)
        p1 = baker.make_recipe('main.apps.portfolio.bank_account', category=category, institution=institution, product=product, currency=Currency.get_czk())
        p1.clean()
        self.assertTrue(True)  # pokud mi neraisoval clean ValidationError, tak je to OK

    def test_clean_category_product_fail(self):
        category = baker.make('categories.Category')
        product = baker.make('products.Product', currencies=[Currency.get_czk()])
        p1 = baker.make_recipe('main.apps.portfolio.portfolio', category=category, product=product, currency=Currency.get_czk())
        with self.assertRaises(ValidationError):
            p1.clean()

    def test_clean_category_product_success(self):
        category = baker.make('categories.Category')
        product = baker.make('products.Product', category=category, currencies=[Currency.get_czk()])
        p1 = baker.make_recipe('main.apps.portfolio.portfolio', category=category, product=product, currency=Currency.get_czk())
        p1.clean()
        self.assertTrue(True)

    def test_clean_product_institution_fail(self):
        institution = baker.make('institutions.Institution', categories=[Category.get_bank_account()])
        product = baker.make('products.Product', category=Category.get_bank_account(), currencies=[Currency.get_czk()])
        p1 = baker.make_recipe('main.apps.portfolio.portfolio', product=product, institution=institution)
        with self.assertRaises(ValidationError):
            p1.clean()

    def test_clean_product_institution_currencies_success(self):
        institution = baker.make('institutions.Institution', categories=[Category.get_bank_account()])
        product = baker.make('products.Product', category=Category.get_bank_account(), currencies=[Currency.get_czk()], institutions=[institution])
        p1 = baker.make_recipe('main.apps.portfolio.portfolio', product=product, institution=institution, category=Category.get_bank_account(), currency=Currency.get_czk())
        p1.clean()
        self.assertTrue(True)

    def test_clean_product_currency_fail(self):
        product = baker.make('products.Product', category=Category.get_bank_account(), currencies=[Currency.get_czk()])
        p1 = baker.make_recipe('main.apps.portfolio.portfolio', product=product, category=Category.get_bank_account())
        with self.assertRaises(ValidationError):
            p1.clean()