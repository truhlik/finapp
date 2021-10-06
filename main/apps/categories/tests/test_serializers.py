from django.test import TestCase
from model_bakery import baker

from main.apps.categories.models import Category
from main.apps.categories.serializers import CategorySerializer


class CategorySerializerTestCase(TestCase):

    def test_values_without_image(self):
        category = baker.make(Category, name='test')
        serializer = CategorySerializer(category)
        exp_data = {
            'slug': category.slug,
            'name': 'test',
            'icon': '',
        }
        self.assertEqual(exp_data, serializer.data)

    def test_values_with_image(self):
        category = baker.make(Category, name='test', icon='categories/icons/test.png')
        serializer = CategorySerializer(category)
        exp_data = {
            'slug': category.slug,
            'name': 'test',
            'icon': 'http://example.com/media/categories/icons/test.png',
        }
        self.assertEqual(exp_data, serializer.data)
