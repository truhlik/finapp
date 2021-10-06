from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.institutions.models import Institution


class InstitutionViewSetTestCase(APITestCase):

    def test_retrieve(self):
        institution = baker.make(Institution, name='test', active=True)
        r = self.client.get(reverse('institution-detail', args=(institution.id, )))
        self.assertEqual(200, r.status_code)
        self.assertEqual(institution.id, r.data['id'])

    def test_list(self):
        baker.make(Institution, name='test', active=True)
        baker.make(Institution, name='test2', active=True)
        baker.make(Institution, name='test2', active=False)
        r = self.client.get(reverse('institution-list'))
        self.assertEqual(200, r.status_code)
        self.assertEqual(2, r.data['pagination']['count'])
        self.assertEqual(2, len(r.data['results']))

    def test_post(self):
        data = {
            'name': 'test',
        }
        r = self.client.post(reverse('institution-list'), data=data)
        self.assertEqual(405, r.status_code)

    def test_delete(self):
        institution = baker.make(Institution, name='test', active=True)
        r = self.client.delete(reverse('institution-detail', args=(institution.id, )))
        self.assertEqual(405, r.status_code)

    def test_patch(self):
        institution = baker.make(Institution, name='test', active=True)
        r = self.client.patch(reverse('institution-detail', args=(institution.id, )))
        self.assertEqual(405, r.status_code)
