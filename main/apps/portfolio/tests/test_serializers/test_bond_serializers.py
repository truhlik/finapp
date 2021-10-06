from model_bakery import baker

from ..helpers import BaseTestCase
from ...constants import PAYMENT_FREQUENCY_YEARLY
from ...models import Bond
from ...serializers import BondsSerializer
from ....categories.models import Category


class BondsSerializerTestCase(BaseTestCase):
    serializer_class = BondsSerializer
    model_class = Bond

    def get_category_instance(self):
        return Category.get_bond()

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
                               )
        serializer = self.get_serializer_class()(portfolio)
        exp_data = {
            'id': portfolio.id,
            'name': 'test',
            'category_obj': {
                'slug': 'bonds',
                'name': 'Dluhopisy',
                'icon': 'http://example.com/media/categories/icons/bonds.png',
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
                'evaluation': 3,
            },
            'currency_obj': {
                    'code': 'CZK',
                    'name': 'Kč'
                },
            'product_id': product.id,
            'currency_id': self.get_currency().code,
            'units': 1000.0,
            'evaluation': 0.01,
            'payment_frequency': PAYMENT_FREQUENCY_YEARLY,
            'start_date': None,
            'end_date': None,
        }
        self.assertEqual(exp_data, serializer.data)

    def test_valid_success(self):
        data = {
            'name': 'test',
            'currency_id': self.get_currency().code,
            'units': 1000,
            'evaluation': 0.01,
            'payment_frequency': PAYMENT_FREQUENCY_YEARLY,
        }
        serializer = self.get_serializer_class()(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

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
            'payment_frequency': PAYMENT_FREQUENCY_YEARLY,
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
            'payment_frequency': PAYMENT_FREQUENCY_YEARLY,
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
            'payment_frequency': PAYMENT_FREQUENCY_YEARLY,
        }
        serializer = self.get_serializer_class()(data=data, context={'request': self.get_request_with_user()})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        instance = serializer.save()
        self.assertEqual(instance.category, self.get_category_instance())
        self.assertEqual(instance.units, 1000)
        self.assertEqual(instance.evaluation, 0.01)
        self.assertEqual(instance.owner, self.get_user())
