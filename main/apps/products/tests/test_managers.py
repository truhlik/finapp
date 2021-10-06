from django.test import TestCase
from model_bakery import baker

from main.apps.products.models import Product


class ProductQuerySetTestCase(TestCase):

    def test_active(self):
        i1 = baker.make(Product, active=True)
        i2 = baker.make(Product, active=False)
        qs = Product.objects.active()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])
