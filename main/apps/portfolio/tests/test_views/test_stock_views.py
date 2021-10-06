from django.urls import reverse
from model_bakery import baker

from main.apps.categories.models import Category
from main.apps.currencies.models import Currency

from ..helpers import BaseTestCase
from ...models import Stock, Portfolio


class StockViewSetUnauthorizedTestCase(BaseTestCase):
    view_basename = 'stock'
    model_class = Stock
    recipe_name = 'stock'

    def get_category_instance(self):
        return Category.get_stock()

    def test_retrieve(self):
        obj = baker.make_recipe('main.apps.portfolio.{}'.format(self.recipe_name), category=self.get_category_instance(), active=True, owner=self.get_user())
        r = self.client.get(reverse('{}-detail'.format(self.view_basename), args=(obj.id, )))
        self.assertEqual(401, r.status_code)

    def test_list(self):
        baker.make_recipe('main.apps.portfolio.{}'.format(self.recipe_name), category=self.get_category_instance(), active=True, owner=self.get_user())
        baker.make(Portfolio, category=Category.get_bank_account(), active=True, owner=self.get_user())
        baker.make_recipe('main.apps.portfolio.{}'.format(self.recipe_name), category=self.get_category_instance(), active=True)
        baker.make_recipe('main.apps.portfolio.{}'.format(self.recipe_name), category=self.get_category_instance(), active=False, owner=self.get_user())
        r = self.client.get(reverse('{}-list'.format(self.view_basename)))
        self.assertEqual(401, r.status_code)

    def test_post(self):
        data = {
            'name': 'test',
        }
        r = self.client.post(reverse('{}-list'.format(self.view_basename)), data=data)
        self.assertEqual(401, r.status_code)

    def test_delete(self):
        obj = baker.make_recipe('main.apps.portfolio.{}'.format(self.recipe_name), category=self.get_category_instance(), active=True)
        r = self.client.delete(reverse('{}-detail'.format(self.view_basename), args=(obj.id, )))
        self.assertEqual(401, r.status_code)

    def test_patch(self):
        obj = baker.make_recipe('main.apps.portfolio.{}'.format(self.recipe_name), category=self.get_category_instance(), active=True)
        r = self.client.patch(reverse('{}-detail'.format(self.view_basename), args=(obj.id, )))
        self.assertEqual(401, r.status_code)


class StockViewSetAuthorizedTestCase(BaseTestCase):
    view_basename = 'stock'
    model_class = Stock
    recipe_name = 'stock'

    def get_category_instance(self):
        return Category.get_stock()

    def test_retrieve(self):
        obj = baker.make_recipe('main.apps.portfolio.{}'.format(self.recipe_name), category=self.get_category_instance(), active=True, owner=self.get_user())
        self.client.force_authenticate(self.get_user())
        r = self.client.get(reverse('{}-detail'.format(self.view_basename), args=(obj.id, )))
        self.assertEqual(200, r.status_code)
        self.assertEqual(obj.id, r.data['id'])

    def test_list(self):
        p1 = baker.make_recipe('main.apps.portfolio.{}'.format(self.recipe_name), category=self.get_category_instance(), active=True, owner=self.get_user())
        baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_bank_account(), active=True, owner=self.get_user())
        baker.make_recipe('main.apps.portfolio.{}'.format(self.recipe_name), category=self.get_category_instance(), active=True)
        baker.make_recipe('main.apps.portfolio.{}'.format(self.recipe_name), category=self.get_category_instance(), active=False, owner=self.get_user())
        self.client.force_authenticate(self.get_user())
        r = self.client.get(reverse('{}-list'.format(self.view_basename)))
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(p1.id, r.data['results'][0]['id'])

    def test_post(self):
        institution = self.get_institution()
        product = self.get_product()

        data = {
            'product_id': product.id,
            'units': 1000,
            'name': 'test',
            'evaluation': 0.01,
            'currency_id': self.get_currency().code,
        }
        self.client.force_authenticate(self.get_user())
        r = self.client.post(reverse('{}-list'.format(self.view_basename)), data=data)
        self.assertEqual(201, r.status_code)

    def test_delete(self):
        self.client.force_authenticate(self.get_user())
        obj = baker.make_recipe('main.apps.portfolio.{}'.format(self.recipe_name), category=self.get_category_instance(), active=True, owner=self.get_user())
        r = self.client.delete(reverse('{}-detail'.format(self.view_basename), args=(obj.id, )))
        self.assertEqual(204, r.status_code)

    def test_patch(self):
        institution = self.get_institution()
        product = baker.make_recipe('main.apps.products.product',
                                    category=self.get_category_instance(),
                                    currencies=[Currency.get_czk()], institutions=[institution])

        obj = baker.make_recipe('main.apps.portfolio.{}'.format(self.recipe_name),
                                category=self.get_category_instance(),
                                active=True,
                                owner=self.get_user(),
                                currency=Currency.get_czk(),
                                institution=institution,
                                product=product)

        data = {
            'product_id': product.id,
            'units': 1000,
            'name': 'test',
            'evaluation': 0.01,
            'currency_id': self.get_currency().code,
        }
        self.client.force_authenticate(self.get_user())
        r = self.client.patch(reverse('{}-detail'.format(self.view_basename), args=(obj.id, )), data=data)
        self.assertEqual(200, r.status_code)
