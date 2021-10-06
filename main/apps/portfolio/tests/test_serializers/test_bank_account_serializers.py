from model_bakery import baker

from ..helpers import BaseTestCase
from ...models import BankAccount
from ...serializers import BankAccountsSerializer
from ....categories.models import Category


class BankAccountsSerializerTestCase(BaseTestCase):
    serializer_class = BankAccountsSerializer
    model_class = BankAccount
    maxDiff = None

    def get_category_instance(self):
        return Category.get_bank_account()

    def test_values(self):
        institution = self.get_institution()
        product = self.get_product()
        portfolio = baker.make(self.get_model_class(),
                               name='test',
                               category=self.get_category_instance(),
                               institution=institution,
                               product=product,
                               currency=self.get_currency(),
                               units=1000,
                               evaluation=0.01,
                               data={
                                   "account_number": "123456789/0800",
                               },
                               )
        serializer = self.get_serializer_class()(portfolio)
        exp_data = {
            'id': portfolio.id,
            'name': 'test',
            'category_obj': {
                'slug': 'bank-accounts',
                'name': 'Běžné účty',
                'icon': 'http://example.com/media/categories/icons/bank-accounts.png',
            },
            'institution_obj': {
                'id': institution.id,
                'name': 'test',
            },
            'product_obj': {
                'id': product.id,
                'name': 'test',
                'currencies': [
                    {
                        'code': 'CZK',
                        'name': 'Kč'
                    }
                ],
                'evaluation': 3.0,
            },
            'currency_obj': {
                'code': 'CZK',
                'name': 'Kč'
            },
            'institution_id': institution.id,
            'product_id': product.id,
            'currency_id': self.get_currency().code,
            'units': 1000.0,
            'account_number': "123456789/0800",
            'evaluation': 0.01,
            'income': None,
            'outcome': None,
        }
        self.assertEqual(exp_data, serializer.data)

    def test_valid_success(self):
        institution = self.get_institution()
        product = self.get_product()
        data = {
            'name': 'test',
            'institution_id': institution.id,
            'product_id': product.id,
            'currency_id': self.get_currency().code,
            'units': 1000,
            'evaluation': 0.01,
            'account_number': "",
            'income': None,
            'outcome': None,
        }
        serializer = self.get_serializer_class()(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_valid_institution_category(self):
        institution = self.get_institution(with_category=False)
        product = self.get_product()
        data = {
            'name': 'test',
            'institution_id': institution.id,
            'product_id': product.id,
            'currency_id': self.get_currency().code,
            'units': 1000,
            'account_number': "123456789/0800",
            'evaluation': 0.01,
        }
        serializer = self.get_serializer_class()(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('institution_id', serializer.errors.keys())

    def test_valid_product_category(self):
        institution = self.get_institution()
        product = self.get_product(with_category=False)
        data = {
            'name': 'test',
            'institution_id': institution.id,
            'product_id': product.id,
            'currency_id': self.get_currency().code,
            'units': 1000,
            'account_number': "123456789/0800",
            'evaluation': 0.01,
        }
        serializer = self.get_serializer_class()(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('product_id', serializer.errors.keys())

    def test_valid_product_institution(self):
        institution = self.get_institution()
        product = self.get_product(with_institution=False)
        data = {
            'name': 'test',
            'institution_id': institution.id,
            'product_id': product.id,
            'currency_id': self.get_currency().code,
            'units': 1000,
            'account_number': "123456789/0800",
            'evaluation': 0.01,
        }
        serializer = self.get_serializer_class()(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('product_id', serializer.errors.keys())

    def test_valid_product_currency(self):
        institution = self.get_institution()
        product = self.get_product(with_currency=False)
        data = {
            'name': 'test',
            'institution_id': institution.id,
            'product_id': product.id,
            'currency_id': self.get_currency().code,
            'units': 1000,
            'account_number': "123456789/0800",
            'evaluation': 0.01,
        }
        serializer = self.get_serializer_class()(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('currency_id', serializer.errors.keys())

    def test_create(self):
        institution = self.get_institution()
        product = self.get_product()
        data = {
            'name': 'test',
            'institution_id': institution.id,
            'product_id': product.id,
            'currency_id': self.get_currency().code,
            'units': 1000,
            'account_number': "123456789/0800",
            'evaluation': 0.01,
            'income': 10000,
            'outcome': 20000,
        }
        serializer = self.get_serializer_class()(data=data, context={'request': self.get_request_with_user()})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        instance = serializer.save()
        self.assertEqual(instance.category, self.get_category_instance())
        self.assertEqual(instance.units, 1000)
        self.assertEqual(instance.evaluation, 0.01)
        self.assertEqual(instance.data, {'account_number': "123456789/0800", "income": 10000, "outcome": 20000})
        self.assertEqual(instance.owner, self.get_user())
        self.assertEqual(0.01, instance.current_eval)

    def test_update(self):
        institution = self.get_institution()
        product = self.get_product()
        obj = baker.make(self.get_model_class(),
                         name='test',
                         category=self.get_category_instance(),
                         institution=institution,
                         product=product,
                         currency=self.get_currency(),
                         units=1000,
                         data={
                             "account_number": "123456789/0800",
                             "evaluation": 0.01,
                         },
                         )
        data = {
            "units": 2000,
        }
        serializer = self.get_serializer_class()(instance=obj,
                                                 partial=True,
                                                 data=data,
                                                 context={'request': self.get_request_with_user()})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        obj = serializer.save()
        self.assertEqual(2000, obj.value)
