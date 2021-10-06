from django.utils import timezone
from model_bakery import baker

from ..helpers import BaseTestCase
from ...constants import PAYMENT_FREQUENCY_MONTH
from ...models import BuildingSaving
from ...serializers import BuildingSavingSerializer
from ....categories.models import Category


class BuildingSavingsSerializerTestCase(BaseTestCase):
    serializer_class = BuildingSavingSerializer
    model_class = BuildingSaving

    def get_category_instance(self):
        return Category.get_building_saving()

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
                               data={'payment_frequency': PAYMENT_FREQUENCY_MONTH, 'income': 1500}
                               )
        serializer = self.get_serializer_class()(portfolio)
        exp_data = {
            'id': portfolio.id,
            'name': 'test',
            'category_obj': {
                'slug': 'building-savings',
                'name': 'Stavební spoření',
                'icon': 'http://example.com/media/categories/icons/building-savings.png',
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
            'final_sum': None,
            'initial_sum': None,
            'payment_frequency': PAYMENT_FREQUENCY_MONTH,
            'income': 1500,
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
            'payment_frequency': PAYMENT_FREQUENCY_MONTH,
            'income': 1500,
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
            'payment_frequency': PAYMENT_FREQUENCY_MONTH,
            'income': 1500,
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
            'payment_frequency': PAYMENT_FREQUENCY_MONTH,
            'income': 1500,
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
            'payment_frequency': PAYMENT_FREQUENCY_MONTH,
            'income': 1500,
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
            'final_sum': 20000,
            'initial_sum': 10000,
            'start_date': (timezone.now().date() + timezone.timedelta(days=365*3)).isoformat(),
            'payment_frequency': PAYMENT_FREQUENCY_MONTH,
            'income': 1500,
        }
        serializer = self.get_serializer_class()(data=data, context={'request': self.get_request_with_user()})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        instance = serializer.save()
        self.assertEqual(self.get_category_instance(), instance.category)
        self.assertEqual(1000, instance.units, 1000)
        self.assertEqual(0.01, instance.evaluation, 0.01)
        self.assertEqual(self.get_user(), instance.owner)
        self.assertEqual(20000, instance.final_sum)
        self.assertEqual(10000, instance.initial_sum)
        self.assertEqual((timezone.now() + timezone.timedelta(days=365*3)).date(), instance.start_date)
