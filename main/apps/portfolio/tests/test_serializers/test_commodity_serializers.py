from django.utils import timezone
from model_bakery import baker

from ..helpers import BaseTestCase
from ...models import Commodity
from ...serializers import CommoditySerializer
from ....categories.models import Category


class CommoditiesSerializerTestCase(BaseTestCase):
    serializer_class = CommoditySerializer
    model_class = Commodity

    def get_category_instance(self):
        return Category.get_commodity()

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
                'slug': 'commodities',
                'name': 'Komodity',
                'icon': 'http://example.com/media/categories/icons/commodities.png',
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
            'buy_price': None,
            'income': None,
            'start_date': None,
        }
        self.assertEqual(exp_data, serializer.data)

    def test_valid_success(self):
        product = self.get_product()
        data = {
            'product_id': product.id,
            'units': 1000,
            'name': 'test',
            'evaluation': 0.01,
            'currency_id': self.get_currency().code,
            'start_date': None,
        }
        serializer = self.get_serializer_class()(data=data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_valid_product_category(self):
        product = self.get_product(with_category=False)
        data = {
            'product_id': product.id,
            'units': 1000,
            'name': 'test',
            'evaluation': 0.01,
            'currency_id': self.get_currency().code,
        }
        serializer = self.get_serializer_class()(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('product_id', serializer.errors.keys())

    def test_valid_product_currency(self):
        product = self.get_product(with_currency=False)
        data = {
            'product_id': product.id,
            'units': 1000,
            'name': 'test',
            'evaluation': 0.01,
            'currency_id': self.get_currency().code,
        }
        serializer = self.get_serializer_class()(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('currency_id', serializer.errors.keys())

    def test_create(self):
        product = self.get_product()
        data = {
            'product_id': product.id,
            'units': 1000,
            'name': 'test',
            'evaluation': 0.01,
            'currency_id': self.get_currency().code,
            'buy_price': 10,
            'income': 1000,
            'start_date': (timezone.now().date() - timezone.timedelta(days=365*3)).isoformat(),
        }
        serializer = self.get_serializer_class()(data=data, context={'request': self.get_request_with_user()})
        self.assertTrue(serializer.is_valid(raise_exception=True))
        instance = serializer.save()
        self.assertEqual(self.get_category_instance(), instance.category)
        self.assertEqual(1000, instance.units)
        self.assertEqual(0.01, instance.evaluation)
        self.assertEqual(self.get_user(), instance.owner)
        self.assertEqual(10.0, instance.buy_price)
        self.assertEqual(1000, instance.income)
        self.assertEqual((timezone.now() - timezone.timedelta(days=365 * 3)).date(), instance.start_date)
