from django.test import TestCase
from model_bakery import baker

from main.apps.institutions.models import Institution
from main.apps.institutions.serializers import InstitutionSerializer


class CategorySerializerTestCase(TestCase):

    def test_values(self):
        institution = baker.make(Institution, name='test')
        serializer = InstitutionSerializer(institution)
        exp_data = {
            'id': institution.id,
            'name': 'test',
        }
        self.assertEqual(exp_data, serializer.data)
