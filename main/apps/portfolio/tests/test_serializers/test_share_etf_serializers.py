from django.utils import timezone
from model_bakery import baker

from ..helpers import BaseTestCase
from ...constants import STRATEGY_DYNAMIC
from ...models import ShareEtf
from ...serializers import ShareEtfSerializer
from ....categories.models import Category


class ShareEtfSerializerTestCase(BaseTestCase):
    serializer_class = ShareEtfSerializer
    model_class = ShareEtf

    def get_category_instance(self):
        return Category.get_share_etf()

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
                                   'income': 1000,
                               }
                               )
        serializer = self.get_serializer_class()(portfolio)
        exp_data = {
            'id': portfolio.id,
            'name': 'test',
            'category_obj': {
                'slug': 'share-etf',
                'name': 'Podílové listy / ETF',
                'icon': 'http://example.com/media/categories/icons/share-etf.png',
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
            'institution_obj': {
                'id': institution.id,
                'name': 'test',

            },
            'institution_id': institution.id,
            'product_id': product.id,
            'currency_id': self.get_currency().code,
            'units': 1000.0,
            'evaluation': 0.01,
            'start_date': None,
            'actual_sum': None,
            'initial_sum': None,
            'saving_strategy': None,
            'income': 1000,
        }
        self.assertEqual(exp_data, serializer.data)

    def test_valid_success(self):
        product = self.get_product()
        institution = self.get_institution()
        data = {
            'institution_id': institution.id,
            'product_id': product.id,
            'units': 1000,
            'evaluation': 0.01,
            'name': 'test',
            'currency_id': self.get_currency().code,
            'income': 1000,
            'income_employer': 1500,
            'saving_strategy': "",
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
            'evaluation': 0.01,
            'income': 1000,
            'income_employer': 1500,
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
            'evaluation': 0.01,
            'income': 1000,
            'income_employer': 1500,
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
            'evaluation': 0.01,
            'income': 1000,
            'income_employer': 1500,
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
            'evaluation': 0.01,
            'initial_sum': 10000,
            'start_date': (timezone.now().date() + timezone.timedelta(days=365*3)).isoformat(),
            'saving_strategy': STRATEGY_DYNAMIC,
            'income': 1000,
        }
        serializer = self.get_serializer_class()(data=data, context={'request': self.get_request_with_user()})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        instance = serializer.save()
        self.assertEqual(self.get_category_instance(), instance.category)
        self.assertEqual(1000, instance.units)
        self.assertEqual(0.01, instance.evaluation)
        self.assertEqual(self.get_user(), instance.owner)
        self.assertEqual(10000, instance.initial_sum)
        self.assertEqual(1000, instance.income)
        self.assertEqual(STRATEGY_DYNAMIC, instance.saving_strategy)
        self.assertEqual((timezone.now() + timezone.timedelta(days=365*3)).date(), instance.start_date)
