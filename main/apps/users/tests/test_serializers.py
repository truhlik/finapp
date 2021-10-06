from django.test import TestCase
from unittest import mock

from model_bakery import baker
from rest_framework.test import APIRequestFactory

from ..models import User
from ..serializers import UserSerializer, UserRegisterSerializer


class UserSerializersTestCase(TestCase):

    def setUp(self) -> None:
        super(UserSerializersTestCase, self).setUp()

    def test_user_serializer_keys(self):
        c1 = baker.make('users.User')
        self.assertEqual(
            [
                'id',
                'first_name',
                'last_name',
                'street',
                'number',
                'city',
                'zip',
                'address',
                'invoice_name',
                'invoice_street',
                'invoice_number',
                'invoice_city',
                'invoice_zip',
                'vat_number',
                'reg_number',
                'email',
                'phone',
            ],
            list(UserSerializer(c1).data.keys())
        )

    def test_validation(self):
        data = {
            'first_name': 'test',
            'last_name': 'test',
            'street': 'test',
            'number': 'test',
            'city': 'test',
            'zip': 'test',
            'invoice_name': 'test',
            'invoice_street': 'test',
            'invoice_number': 'test',
            'invoice_city': 'test',
            'invoice_zip': 'test',
            'vat_number': 'test',
            'reg_number': 'test',
            'email': 'test@test.cz',
        }
        self.assertTrue(UserSerializer(data=data).is_valid())

    # email je read only, takze se nevaliduje
    # def test_validation_email_failed(self):
    #     baker.make('users.User', email='test@test.cz')
    #     data = {
    #         'first_name': 'test',
    #         'last_name': 'test',
    #         'street': 'test',
    #         'number': 'test',
    #         'city': 'test',
    #         'zip': 'test',
    #         'invoice_name': 'test',
    #         'invoice_street': 'test',
    #         'invoice_number': 'test',
    #         'invoice_city': 'test',
    #         'invoice_zip': 'test',
    #         'vat_number': 'test',
    #         'reg_number': 'test',
    #         'email': 'test@test.cz',
    #     }
    #     serializer = UserSerializer(data=data)
    #     self.assertFalse(serializer.is_valid())
    #     self.assertIn('email', serializer.errors.keys())

    def test_validation_email_success_for_self(self):
        u = baker.make('users.User', email='test@test.cz')
        data = {
            'first_name': 'test',
            'last_name': 'test',
            'street': 'test',
            'number': 'test',
            'city': 'test',
            'zip': 'test',
            'invoice_name': 'test',
            'invoice_street': 'test',
            'invoice_number': 'test',
            'invoice_city': 'test',
            'invoice_zip': 'test',
            'vat_number': 'test',
            'reg_number': 'test',
            'email': 'test@test.cz',
        }
        serializer = UserSerializer(instance=u, data=data)
        self.assertTrue(serializer.is_valid())

    def test_save(self):
        data = {
            'first_name': 'test',
            'last_name': 'test',
            'street': 'Husova',
            'number': '579',
            'city': 'Kralupy nad Vltavou',
            'zip': '27801',
            'invoice_name': 'test',
            'invoice_street': 'test',
            'invoice_number': 'test',
            'invoice_city': 'test',
            'invoice_zip': 'test',
            'vat_number': 'test',
            'reg_number': 'test',
            'email': 'test@test.cz',
        }
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        qs = User.objects.all()
        self.assertEqual(1, len(qs))

    def test_email_read_only(self):
        u = baker.make(User, email='test@test.cz')
        serializer = UserSerializer(instance=u, data={"email": "ahojky@jaksemate.cz"}, partial=True)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        serializer.save()
        u.refresh_from_db()
        self.assertEqual('test@test.cz', u.email)


class UserRegisterSerializerTestCase(TestCase):

    def setUp(self) -> None:
        super(UserRegisterSerializerTestCase, self).setUp()

    def test_keys(self):
        user = baker.make('users.User')
        serializer = UserRegisterSerializer(instance=user)
        self.assertEqual(
            ['email'],
            list(serializer.data.keys())
        )

    def test_validation_success(self):
        data = {
            'email': 'test@test.cz',
            'password1': 'KreativniHeslo1234',
            'password2': 'KreativniHeslo1234',
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_validation_failed(self):
        baker.make('users.User', email='test@test.cz')
        data = {
            'email': 'test@test.cz',
            'password1': 'Trubaduri2020',
            'password2': 'Trubaduri2020',
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_save(self):
        factory = APIRequestFactory()
        request = factory.get('/')
        request.session = {}
        data = {
            'email': 'test@test.cz',
            'password1': 'Test1234',
            'password2': 'Test1234',
        }
        serializer = UserRegisterSerializer(data=data)
        serializer.is_valid()
        serializer.save(request=request)
        qs = User.objects.all()
        self.assertEqual(1, len(qs))
