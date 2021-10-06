from django.conf import settings
from django.test import TestCase
from model_bakery import baker

from ..models import Product
from ..serializers import ProductSerializer
from ...currencies.models import Currency


class ProductSerializerTestCase(TestCase):
    fixtures = ['currencies.json']

    def test_values(self):
        product = baker.make(Product, name='test', currencies=[Currency.get_czk()], evaluation=1)
        serializer = ProductSerializer(product)
        exp_data = {
            'id': product.id,
            'name': 'test',
            'currencies': [
                {
                    'code': 'CZK',
                    'name': 'Kč'
                }
            ],
            'evaluation': 1.0,
        }
        self.assertEqual(exp_data, serializer.data)
