from django.urls import reverse, NoReverseMatch
from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.categories.models import Category


class PortfolioViewSetTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = baker.make('users.User')

    def test_retrieve(self):
        obj = baker.make_recipe('main.apps.portfolio.portfolio', name='test', active=True, owner=self.user)
        self.client.force_authenticate(self.user)
        r = self.client.get(reverse('portfolio-detail', args=(obj.id, )))
        self.assertEqual(200, r.status_code)
        self.assertEqual(obj.id, r.data['id'])

    def test_list(self):
        p1 = baker.make_recipe('main.apps.portfolio.portfolio', name='test', active=True, owner=self.user)
        baker.make_recipe('main.apps.portfolio.portfolio', name='test2', active=True)
        baker.make_recipe('main.apps.portfolio.portfolio', name='test2', active=False)
        self.client.force_authenticate(self.user)
        r = self.client.get(reverse('portfolio-list'))
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(p1.id, r.data['results'][0]['id'])

    def test_post(self):
        data = {
            'name': 'test',
        }
        self.client.force_authenticate(self.user)
        r = self.client.post(reverse('portfolio-list'), data=data)
        self.assertEqual(405, r.status_code)

    def test_delete(self):
        self.client.force_authenticate(self.user)
        obj = baker.make_recipe('main.apps.portfolio.portfolio', name='test', active=True)
        r = self.client.delete(reverse('portfolio-detail', args=(obj.id, )))
        self.assertEqual(405, r.status_code)

    def test_patch(self):
        self.client.force_authenticate(self.user)
        obj = baker.make_recipe('main.apps.portfolio.portfolio', name='test', active=True)
        r = self.client.patch(reverse('portfolio-detail', args=(obj.id, )))
        self.assertEqual(405, r.status_code)


class PortfolioGroupByViewSet(APITestCase):
    fixtures = ['categories.json', 'currencies.json']

    def setUp(self) -> None:
        self.user = baker.make('users.User')

    def test_retrieve(self):
        obj = baker.make_recipe('main.apps.portfolio.portfolio', name='test', active=True, owner=self.user)
        self.client.force_authenticate(self.user)
        with self.assertRaises(NoReverseMatch):
            r = self.client.get(reverse('portfolio-group-detail', args=(obj.id, )))
            self.assertEqual(200, r.status_code)
            self.assertEqual(obj.id, r.data['id'])

    def test_list(self):
        p1 = baker.make_recipe('main.apps.portfolio.portfolio', name='test', active=True, value=2, current_eval=2, owner=self.user)
        baker.make_recipe('main.apps.portfolio.portfolio', name='test2', active=True, value=1, current_eval=1, owner=self.user)
        baker.make_recipe('main.apps.portfolio.portfolio', name='test2', active=True, value=1, current_eval=1)
        self.client.force_authenticate(self.user)
        r = self.client.get(reverse('portfolio-group-list'))
        self.assertEqual(200, r.status_code)
        self.assertEqual(2, len(r.data['results']))

    def test_list_with_category_slug_filter(self):
        p1 = baker.make_recipe('main.apps.portfolio.portfolio', name='test', active=True, value=2, current_eval=2, owner=self.user, category=Category.get_stock())
        baker.make_recipe('main.apps.portfolio.portfolio', name='test2', active=True, value=1, current_eval=1, owner=self.user, category=Category.get_bank_account())
        baker.make_recipe('main.apps.portfolio.portfolio', name='test2', active=True, value=1, current_eval=1, category=Category.get_stock())
        self.client.force_authenticate(self.user)
        r = self.client.get(reverse('portfolio-group-list') + '?category_id=stocks')
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, len(r.data['results']))
        self.assertEqual(p1.id, r.data['results'][0]['portfolio_id'])

    def test_list_with_portfolio_id_filter(self):
        p1 = baker.make_recipe('main.apps.portfolio.portfolio', name='test', active=True, value=2, current_eval=2, owner=self.user, category=Category.get_stock())
        baker.make_recipe('main.apps.portfolio.portfolio', name='test2', active=True, value=1, current_eval=1, owner=self.user, category=Category.get_bank_account())
        baker.make_recipe('main.apps.portfolio.portfolio', name='test2', active=True, value=1, current_eval=1, category=Category.get_stock())
        self.client.force_authenticate(self.user)
        r = self.client.get(reverse('portfolio-group-list') + '?id={}'.format(p1.id))
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, len(r.data['results']))
        self.assertEqual(p1.id, r.data['results'][0]['portfolio_id'])

    def test_post(self):
        data = {
            'name': 'test',
        }
        self.client.force_authenticate(self.user)
        r = self.client.post(reverse('portfolio-group-list'), data=data)
        self.assertEqual(405, r.status_code)

    def test_delete(self):
        self.client.force_authenticate(self.user)
        obj = baker.make_recipe('main.apps.portfolio.portfolio', name='test', active=True)
        with self.assertRaises(NoReverseMatch):
            r = self.client.delete(reverse('portfolio-group-detail', args=(obj.id, )))
            self.assertEqual(405, r.status_code)

    def test_patch(self):
        self.client.force_authenticate(self.user)
        obj = baker.make_recipe('main.apps.portfolio.portfolio', name='test', active=True)
        with self.assertRaises(NoReverseMatch):
            r = self.client.patch(reverse('portfolio-group-detail', args=(obj.id, )))
            self.assertEqual(405, r.status_code)