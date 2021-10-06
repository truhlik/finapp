from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APITestCase

from ..models import Product


class ProductsViewSetAuthTestCase(APITestCase):
    model = Product
    detail_url = 'product-detail'
    list_url = 'product-list'

    def setUp(self) -> None:
        self.user = baker.make('users.User')
        self.client.force_authenticate(self.user)

    def test_retrieve(self):
        obj = baker.make(self.model, name='test', active=True)
        r = self.client.get(reverse(self.detail_url, args=(obj.id, )))
        self.assertEqual(200, r.status_code)
        self.assertEqual(obj.id, r.data['id'])

    def test_list(self):
        baker.make(self.model, name='test', active=True)
        baker.make(self.model, name='test2', active=True)
        baker.make(self.model, name='test2', active=False)
        r = self.client.get(reverse(self.list_url))
        self.assertEqual(200, r.status_code)
        self.assertEqual(2, r.data['pagination']['count'])
        self.assertEqual(2, len(r.data['results']))

    def test_post(self):
        data = {
            'name': 'test',
        }
        r = self.client.post(reverse(self.list_url), data=data)
        self.assertEqual(405, r.status_code)

    def test_delete(self):
        institution = baker.make(self.model, name='test', active=True)
        r = self.client.delete(reverse(self.detail_url, args=(institution.id, )))
        self.assertEqual(405, r.status_code)

    def test_patch(self):
        institution = baker.make(self.model, name='test', active=True)
        r = self.client.patch(reverse(self.detail_url, args=(institution.id, )))
        self.assertEqual(405, r.status_code)


class ProductsViewSetUnAuthTestCase(APITestCase):
    model = Product
    detail_url = 'product-detail'
    list_url = 'product-list'

    def setUp(self) -> None:
        self.user = baker.make('users.User')

    def test_retrieve(self):
        obj = baker.make(self.model, name='test', active=True)
        r = self.client.get(reverse(self.detail_url, args=(obj.id,)))
        self.assertEqual(401, r.status_code)

    def test_list(self):
        baker.make(self.model, name='test', active=True)
        baker.make(self.model, name='test2', active=True)
        baker.make(self.model, name='test2', active=False)
        r = self.client.get(reverse(self.list_url))
        self.assertEqual(401, r.status_code)

    def test_post(self):
        data = {
            'name': 'test',
        }
        r = self.client.post(reverse(self.list_url), data=data)
        self.assertEqual(401, r.status_code)

    def test_delete(self):
        institution = baker.make(self.model, name='test', active=True)
        r = self.client.delete(reverse(self.detail_url, args=(institution.id,)))
        self.assertEqual(401, r.status_code)

    def test_patch(self):
        institution = baker.make(self.model, name='test', active=True)
        r = self.client.patch(reverse(self.detail_url, args=(institution.id,)))
        self.assertEqual(401, r.status_code)
