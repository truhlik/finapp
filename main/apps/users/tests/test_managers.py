from django.test import TestCase

from model_bakery import baker

from main.apps.users.models import User


class UserManagerTestCase(TestCase):

    def setUp(self) -> None:
        super(UserManagerTestCase, self).setUp()

    def test_is_active(self):
        user1 = baker.make('users.User', is_active=True)
        _ = baker.make('users.User', is_active=False)
        qs = User.objects.active()
        self.assertEqual(user1, qs[0])
        self.assertEqual(1, len(qs))

    def test_not_active(self):
        _ = baker.make('users.User', is_active=True)
        user1 = baker.make('users.User', is_active=False)
        qs = User.objects.not_active()
        self.assertEqual(1, len(qs))
        self.assertEqual(user1, qs[0])

    def test_owner(self):
        _ = baker.make('users.User')
        user1 = baker.make('users.User')
        qs = User.objects.owner(user1)
        self.assertEqual(1, len(qs))
        self.assertEqual(user1, qs[0])
