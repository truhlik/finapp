from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.categories.models import Category


class CategoryViewSetTestCase(APITestCase):

    def test_retrieve(self):
        category = baker.make(Category, name='test')
        r = self.client.get(reverse('category-detail', args=(category.slug, )))
        self.assertEqual(200, r.status_code)
        self.assertEqual(category.slug, r.data['slug'])

    def test_list(self):
        baker.make(Category, name='test')
        baker.make(Category, name='test2')
        r = self.client.get(reverse('category-list'))
        self.assertEqual(200, r.status_code)
        self.assertEqual(2, r.data['pagination']['count'])
        self.assertEqual(2, len(r.data['results']))

    def test_post(self):
        data = {
            'name': 'test',
        }
        r = self.client.post(reverse('category-list'), data=data)
        self.assertEqual(405, r.status_code)

    def test_delete(self):
        category = baker.make(Category, name='test')
        r = self.client.delete(reverse('category-detail', args=(category.slug, )))
        self.assertEqual(405, r.status_code)

    def test_patch(self):
        category = baker.make(Category, name='test')
        r = self.client.patch(reverse('category-detail', args=(category.slug, )))
        self.assertEqual(405, r.status_code)
