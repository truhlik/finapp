from django.test import TestCase
from model_bakery import baker

from main.apps.institutions.models import Institution


class InstitutionQuerySetTestCase(TestCase):

    def test_active(self):
        i1 = baker.make(Institution, active=True)
        i2 = baker.make(Institution, active=False)
        qs = Institution.objects.active()
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])
