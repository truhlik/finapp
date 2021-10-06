from allauth.account.models import EmailAddress
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APITestCase
from django.core import mail

from main.apps.users.models import User


def static_coords():
    return 50.2395909, 14.3103825


class UserViewsTestCase(APITestCase):

    def setUp(self) -> None:
        super(UserViewsTestCase, self).setUp()

        self.user = baker.make('users.User', is_active=True)
        self.data = {
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

    def do_auth(self):
        self.client.force_authenticate(user=self.user)

    def test_get(self):
        resp = self.client.get(reverse('user-detail', args=(self.user.id, )))
        self.assertEqual(401, resp.status_code)

    def test_list(self):
        self.do_auth()
        baker.make('users.User', is_active=True)
        baker.make('users.User', is_active=True)
        resp = self.client.get(reverse('user-list'))
        self.assertEqual(200, resp.status_code)
        self.assertEqual(1, resp.data['pagination']['count'])  # jeden je v setUp

    def test_patch(self):
        self.do_auth()
        resp = self.client.patch(reverse('user-detail', args=(self.user.id, )), data=self.data)
        self.assertEqual(200, resp.status_code)

    def test_patch_another_user(self):
        self.do_auth()
        u = baker.make('users.User')
        resp = self.client.patch(reverse('user-detail', args=(u.id, )), data=self.data)
        self.assertEqual(404, resp.status_code)

    def test_get_another_user(self):
        self.do_auth()
        u = baker.make('users.User')
        resp = self.client.get(reverse('user-detail', args=(u.id, )))
        self.assertEqual(404, resp.status_code)

    def test_delete(self):
        self.do_auth()
        resp = self.client.delete(reverse('user-detail', args=(self.user.id, )))
        self.assertEqual(405, resp.status_code)

    def test_delete_another_user(self):
        self.do_auth()
        u = baker.make('users.User')
        resp = self.client.delete(reverse('user-detail', args=(u.id, )))
        self.assertEqual(405, resp.status_code)

    def test_post(self):
        self.do_auth()
        resp = self.client.post(reverse('user-list'))
        self.assertEqual(405, resp.status_code)

    def test_get_self(self):
        self.do_auth()
        resp = self.client.get(reverse('user-self'))
        self.assertEqual(200, resp.status_code)
        self.assertEqual(str(self.user.id), resp.data['id'])

    def test_patch_self(self):
        self.do_auth()
        resp = self.client.patch(reverse('user-self'), data=self.data)
        self.assertEqual(200, resp.status_code)
        self.user.refresh_from_db()
        self.assertEqual('test', self.user.first_name)

    def test_delete_self(self):
        self.do_auth()
        resp = self.client.delete(reverse('user-self'))
        self.assertEqual(405, resp.status_code)


class UserAnonymousViewsTestCase(APITestCase):

    def setUp(self) -> None:
        super(UserAnonymousViewsTestCase, self).setUp()

        self.user = baker.make('users.User', is_active=True)
        self.data = {
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

    def test_get(self):
        resp = self.client.get(reverse('user-detail', args=(self.user.id, )))
        self.assertEqual(401, resp.status_code)

    def test_list(self):
        baker.make('users.User', is_active=True)
        baker.make('users.User', is_active=True)
        resp = self.client.get(reverse('user-list'))
        self.assertEqual(401, resp.status_code)

    def test_patch(self):
        resp = self.client.patch(reverse('user-detail', args=(self.user.id, )), data=self.data)
        self.assertEqual(401, resp.status_code)

    def test_delete(self):
        resp = self.client.delete(reverse('user-detail', args=(self.user.id, )))
        self.assertEqual(401, resp.status_code)

    def test_post(self):
        resp = self.client.post(reverse('user-list'))
        self.assertEqual(401, resp.status_code)

    def test_get_self(self):
        resp = self.client.get(reverse('user-self'))
        self.assertEqual(401, resp.status_code)

    def test_patch_self(self):
        resp = self.client.patch(reverse('user-self'), data=self.data)
        self.assertEqual(401, resp.status_code)

    def test_delete_self(self):
        resp = self.client.delete(reverse('user-self'))
        self.assertEqual(401, resp.status_code)


class AccountsViews(APITestCase):

    def test_registration(self) -> None:
        data = {
            'email': 'test@test.cz',
            'password1': 'KreativniHeslo1234',
            'password2': 'KreativniHeslo1234',
        }
        url = reverse('rest_register')
        resp = self.client.post(url, data=data)
        self.assertEqual(201, resp.status_code)
        qs = User.objects.all()
        self.assertEqual(1, len(qs))

    def test_login_failed(self) -> None:
        data = {
            'email': 'test@test.cz',
            'password': 'Test1234',
        }
        resp = self.client.post(reverse('rest_login'), data=data)
        self.assertEqual(400, resp.status_code)

    def test_login_success(self) -> None:
        user = baker.make('users.User', email='test@test.cz')
        user.set_password('HolaHej4321')
        user.save()
        baker.make(EmailAddress, email=user.email, user=user, verified=True)
        super(AccountsViews, self).setUp()
        data = {
            'email': 'test@test.cz',
            'password': 'HolaHej4321',
        }
        resp = self.client.post(reverse('rest_login'), data=data)
        self.assertEqual(200, resp.status_code)

    def test_password_reset_user_does_not_exists(self):
        data = {
            'email': 'test@test.cz',
        }
        resp = self.client.post(reverse('rest_password_reset'), data=data)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(0, len(mail.outbox))

    def test_password_reset_user_exist(self):
        self.user = baker.make('users.User', is_active=True, email='test@test.cz')
        data = {
            'email': 'test@test.cz',
        }
        resp = self.client.post(reverse('rest_password_reset'), data=data)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(1, len(mail.outbox))

    def test_password_change(self):
        self.user = baker.make('users.User', is_active=True, email='test@test.cz')
        self.client.force_authenticate(user=self.user)
        self.user.set_password('Test1234')
        data = {
            'old_password': 'Test1234',
            'new_password1': 'Ahoj4321',
            'new_password2': 'Ahoj4321',
        }
        resp = self.client.post(reverse('rest_password_change'), data=data)
        self.assertEqual(200, resp.status_code)

    # def test_password_reset_confirm(self):
    #     self.user = baker.make('users.User', is_active=True, email='test@test.cz')
    #     self.client.force_authenticate(user=self.user)
    #     self.user.set_password('Test1234')
    #     data = {
    #         'old_password': 'Test1234',
    #         'new_password1': 'Ahoj4321',
    #         'new_password2': 'Ahoj4321',
    #     }
    #     resp = self.client.post(reverse('rest_password_change'), data=data)
    #     self.assertEqual(200, resp.status_code)
