import datetime
from unittest.mock import patch

from django.urls import reverse
from django.utils import timezone
from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.categories.models import Category


class ListPortfolioValuesByPortfolioViewTestCase(APITestCase):
    fixtures = ['categories.json', 'currencies.json']

    def setUp(self) -> None:
        self.user = baker.make('users.User')

    def test_retrieve(self):
        baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_bank_account(),
                                       owner=self.user, value=10.3333334)
        baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_bank_account(),
                                       owner=self.user, value=5)
        baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_bond(),
                                       owner=self.user, value=2.666666667)

        self.client.force_authenticate(self.user)
        r = self.client.get(reverse('portfolio-chart-pie'))
        self.assertEqual(200, r.status_code)

        exp_lst = {
            'currency': {
                'code': 'CZK',
                'name': 'Kč'
            },
            'data': [
                {
                    'title': Category.get_bank_account().name,
                    'value': 85.19,
                    'data': 15,
                },
                {
                    'title': Category.get_bond().name,
                    'value': 14.81,
                    'data': 2,
                }
            ]
        }
        self.assertEqual(exp_lst, r.json())


class ListPortfolioValuesByDaysViewTestCase(APITestCase):
    fixtures = ['categories.json', 'currencies.json']

    def setUp(self) -> None:
        self.user = baker.make('users.User')

    @patch('main.apps.portfolio_values.methods.timezone')
    def test_retrieve(self, mock_timezone):
        mock_timezone.now.return_value = datetime.datetime(year=2021, month=3, day=11)
        mock_timezone.timedelta.return_value = datetime.timedelta(days=100)

        with patch.object(timezone, 'now', return_value=datetime.datetime(year=2021, month=3, day=11)):

            baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=10.6666667, date=timezone.now().date(),
                       portfolio__category=Category.get_bank_account(), portfolio__owner=self.user)
            baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=20, date=timezone.now().date(),
                       portfolio__category=Category.get_bank_account(), portfolio__owner=self.user)
            baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=5.33333333334,
                              date=timezone.now().date() - timezone.timedelta(days=1),
                       portfolio__category=Category.get_bank_account(), portfolio__owner=self.user)
            baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=15, date=timezone.now().date() - timezone.timedelta(days=1),
                       portfolio__category=Category.get_bond())

        self.client.force_authenticate(self.user)
        r = self.client.get(reverse('portfolio-chart-line'))
        self.assertEqual(200, r.status_code)

        exp_data = {
            'min_y': 2,
            'max_y': 32,
            'min_x': 0,
            'max_x': 2,
            'title_y': [
                {'5': '5 Kč'},
                {'10': '10 Kč'},
                {'15': '15 Kč'},
                {'20': '20 Kč'},
                {'25': '25 Kč'},
                {'30': '30 Kč'}
            ],
            'title_x': [
                {'0': '10 Mar'},
                {'1': '11 Mar'}
            ],
            'currency': {
                'code': 'CZK',
                'name': 'Kč'
            },
            'data': [
                {
                    'date': '2021-03-10',
                    'sum': 5
                },
                {
                    'date': '2021-03-11',
                    'sum': 30
                }
            ]
        }
        self.assertEqual(exp_data, r.json())
