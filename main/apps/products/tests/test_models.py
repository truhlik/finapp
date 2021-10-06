from django.core.exceptions import ValidationError
from django.test import TestCase
from model_bakery import baker

from main.apps.products.models import Product


class ProductModelTestCase(TestCase):

    # def test_clean_category_institution_fail(self):
    #     category = baker.make('categories.Category')
    #     institution = baker.make('institutions.Institution')
    #     p1 = baker.make(Product, active=True, category=category, institutions=[institution])
    #     with self.assertRaises(ValidationError):
    #         p1.clean()

    def test_clean_category_institution_success(self):
        category = baker.make('categories.Category')
        institution = baker.make('institutions.Institution')
        institution.categories.set([category])
        p1 = baker.make(Product, active=True, category=category, institutions=[institution])
        p1.clean()
        self.assertTrue(True)  # pokud mi neraisoval clean ValidationError, tak je to OK
