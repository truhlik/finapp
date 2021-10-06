import datetime
from typing import List
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from main.apps.categories.models import Category
from main.apps.portfolio_values.methods import get_portfolio_values_by_days, get_portfolio_values_by_portfolio, \
    get_meta_data_for_graph
from main.apps.portfolio_values.models import PortfolioValue


class PortfolioValuesUtilsTestCase(TestCase):
    fixtures = ['categories.json']
    maxDiff = None

    def test_get_portfolio_values_empty(self):
        qs = get_portfolio_values_by_days()
        self.assertEqual(0, len(qs))

    def test_get_portfolio_values_without_filtering(self):
        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=10, date=timezone.now().date(),
                   portfolio__category=Category.get_bank_account())
        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=20, date=timezone.now().date(),
                   portfolio__category=Category.get_bank_account())
        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=5, date=timezone.now().date() - timezone.timedelta(days=1),
                   portfolio__category=Category.get_bank_account())
        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=15, date=timezone.now().date() - timezone.timedelta(days=1),
                   portfolio__category=Category.get_bond())
        res: List = get_portfolio_values_by_days()
        exp_lst = [
                {
                    'date': timezone.now().date() - timezone.timedelta(days=1),
                    'sum': 20,
                },
                {
                    'date': timezone.now().date(),
                    'sum': 30,
                },

            ]
        self.assertEqual(exp_lst, list(res))

    def test_get_portfolio_values_with_user_filtering(self):
        user = baker.make('users.User')

        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=10, date=timezone.now().date(),
                   portfolio__category=Category.get_bank_account(), portfolio__owner=user)
        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=20, date=timezone.now().date(),
                   portfolio__category=Category.get_bank_account(), portfolio__owner=user)
        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=5, date=timezone.now().date() - timezone.timedelta(days=1),
                   portfolio__category=Category.get_bank_account(), portfolio__owner=user)
        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=15, date=timezone.now().date() - timezone.timedelta(days=1),
                   portfolio__category=Category.get_bond())
        res: List = get_portfolio_values_by_days(user=user)
        exp_lst = [
                {
                    'date': timezone.now().date() - timezone.timedelta(days=1),
                    'sum': 5,
                },
                {
                    'date': timezone.now().date(),
                    'sum': 30,
                },

            ]
        self.assertEqual(exp_lst, list(res))

    def test_get_portfolio_values_with_days_filtering(self):
        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=10, date=timezone.now().date(),
                   portfolio__category=Category.get_bank_account())
        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=20, date=timezone.now().date(),
                   portfolio__category=Category.get_bank_account())
        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=5, date=timezone.now().date() - timezone.timedelta(days=1),
                   portfolio__category=Category.get_bank_account())
        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=15, date=timezone.now().date() - timezone.timedelta(days=20),
                   portfolio__category=Category.get_bond())
        res: List = get_portfolio_values_by_days(days=10)
        exp_lst = [
                {
                    'date': timezone.now().date() - timezone.timedelta(days=1),
                    'sum': 5,
                },
                {
                    'date': timezone.now().date(),
                    'sum': 30,
                },

            ]
        self.assertEqual(exp_lst, list(res))

    def test_get_portfolio_values_with_category_filtering(self):
        portfolio1 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_bank_account())
        portfolio2 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_bank_account())

        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=10, date=timezone.now().date(), portfolio=portfolio1)
        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=20, date=timezone.now().date(), portfolio=portfolio2)
        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=5, date=timezone.now().date() - timezone.timedelta(days=1), portfolio=portfolio2)
        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=15, date=timezone.now().date() - timezone.timedelta(days=20),
                   portfolio__category=Category.get_bond())
        res: List = get_portfolio_values_by_days(category_slug=Category.get_bank_account().slug)
        exp_lst = [
                {
                    'date': timezone.now().date() - timezone.timedelta(days=1),
                    'sum': 5,
                },
                {
                    'date': timezone.now().date(),
                    'sum': 30,
                },

            ]
        self.assertEqual(exp_lst, list(res))

    def test_get_portfolio_values_with_portfolio_filtering(self):
        portfolio1 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_bank_account())

        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=10, date=timezone.now().date(), portfolio=portfolio1)
        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=20, date=timezone.now().date())
        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=5, date=timezone.now().date() - timezone.timedelta(days=1), portfolio=portfolio1)
        baker.make_recipe('main.apps.portfolio_values.portfolio_value', value=15, date=timezone.now().date() - timezone.timedelta(days=20),
                   portfolio__category=Category.get_bank_account())
        res: List = get_portfolio_values_by_days(portfolio_id=portfolio1.id)
        exp_lst = [
                {
                    'date': timezone.now().date() - timezone.timedelta(days=1),
                    'sum': 5,
                },
                {
                    'date': timezone.now().date(),
                    'sum': 10,
                },

            ]
        self.assertEqual(exp_lst, list(res))

    def test_get_portfolio_values_by_portfolio_empty(self):
        lst = get_portfolio_values_by_portfolio()
        self.assertEqual(0, len(lst))

    def test_get_portfolio_values_by_portfolio_without_filtering(self):
        portfolio1 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_bank_account(), value=10)
        portfolio2 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_bank_account(), value=20)
        portfolio3 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_bond(), value=5)
        portfolio4 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_bond(), value=15)

        res: List = get_portfolio_values_by_portfolio()
        exp_lst = [
                {
                    'title': Category.get_bank_account().name,
                    'value': 30,
                },
                {
                    'title': Category.get_bond().name,
                    'value': 20,
                },

            ]
        self.assertEqual(exp_lst, list(res))

    def test_get_portfolio_values_by_portfolio_with_user_filtering(self):
        user = baker.make('users.User')

        portfolio1 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_bank_account(), owner=user, value=10)
        portfolio2 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_bank_account(), owner=user, value=20)
        portfolio3 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_bond(), owner=user, value=15)
        portfolio4 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_bond(), value=5)

        res: List = get_portfolio_values_by_portfolio(user=user)
        exp_lst = [
                {
                    'title': Category.get_bank_account().name,
                    'value': 30,
                },
                {
                    'title': Category.get_bond().name,
                    'value': 15,
                },

            ]
        self.assertEqual(exp_lst, list(res))

    def test_get_portfolio_values_by_portfolio_with_category_filtering(self):
        portfolio1 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_bank_account(), value=10)
        portfolio2 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_bank_account(), value=5)

        res: List = get_portfolio_values_by_portfolio(category_slug=Category.get_bank_account().slug)
        exp_lst = [
                {
                    'title': portfolio1.name,
                    'value': 10,
                },
                {
                    'title': portfolio2.name,
                    'value': 5,
                },

            ]
        self.assertEqual(exp_lst, list(res))

    def test_get_portfolio_values_by_portfolio_with_portfolio_filtering(self):
        portfolio1 = baker.make_recipe('main.apps.portfolio.portfolio', category=Category.get_bank_account(), name='test', value=10)

        res: List = get_portfolio_values_by_portfolio(portfolio_id=portfolio1.id)
        exp_lst = [
                {
                    'title': 'test',
                    'value': 10,
                },
            ]
        self.assertEqual(exp_lst, list(res))

    @patch('main.apps.portfolio_values.methods.timezone')
    def test_get_meta_data_for_graph_empty(self, mock_timezone):
        self.maxDiff = None
        mock_timezone.now.return_value = datetime.datetime(year=2020, month=2, day=4)

        data = []
        metadata = get_meta_data_for_graph(data)

        exp_meta = {
            "min_y": 0,
            "max_y": 100000,
            "min_x": 1,
            "max_x": 6,
            "currency": {
                "code": "CZK",
                "name": "Kč",
            },
            "title_y": [
                {"20000": "20 000 Kč"},
                {"40000": "40 000 Kč"},
                {"60000": "60 000 Kč"},
                {"80000": "80 000 Kč"},
                {"100000": "100 000 Kč"},
            ],
            "title_x": [{'1': '05 Apr'}, {'2': '05 Jun'}, {'3': '05 Aug'}, {'4': '05 Oct'}, {'5': '05 Dec'}, {'6': '04 Feb'}],
        }
        self.assertEqual(exp_meta, metadata)

    def test_get_meta_data_for_graph_count_1(self):
        data = [
            {
                'date': timezone.datetime(day=2, month=2, year=2021).date(),
                'sum': 10,
            },
        ]
        metadata = get_meta_data_for_graph(data)
        exp_meta = {
            "min_y": 9.0,
            "max_y": 21.0,
            "min_x": 0,
            "max_x": 1,
            "currency": {
                "code": "CZK",
                "name": "Kč",
            },
            "title_y": [
                {"10": "10 Kč"},
                {"12": "12 Kč"},
                {"14": "14 Kč"},
                {"16": "16 Kč"},
                {"18": "18 Kč"},
                {"20": "20 Kč"},
            ],
            "title_x": [
                {'0': '02 Feb'},
            ],
        }
        self.assertEqual(exp_meta, metadata)

    def test_get_meta_data_for_graph_less_than_10(self):
        data = [
            {
                'date': timezone.datetime(day=2, month=2, year=2021).date(),
                'sum': 10,
            },
            {
                'date': timezone.datetime(day=3, month=2, year=2021).date(),
                'sum': 20,
            },
            {
                'date': timezone.datetime(day=4, month=2, year=2021).date(),
                'sum': 30,
            },

        ]
        metadata = get_meta_data_for_graph(data)
        exp_meta = {
            "min_y": 8.0,
            "max_y": 32.0,
            "min_x": 0,
            "max_x": 3,
            "currency": {
                "code": "CZK",
                "name": "Kč",
            },
            "title_y": [
                {"10": "10 Kč"},
                {"14": "14 Kč"},
                {"18": "18 Kč"},
                {"22": "22 Kč"},
                {"26": "26 Kč"},
                {"30": "30 Kč"},
            ],
            "title_x": [
                {'0': '02 Feb'}, {'1': '03 Feb'}, {'2': '04 Feb'},
            ],
        }
        self.assertEqual(exp_meta, metadata)

    def test_get_meta_data_for_graph_more_than_10(self):
        self.maxDiff = None

        data = [
            {
                'date': datetime.datetime(year=2020, month=2, day=4).date() - timezone.timedelta(days=(100 - i)),
                'sum': 10 + i
            }
            for i in range(0, 100)
        ]
        metadata = get_meta_data_for_graph(data)
        exp_meta = {
            "min_y": 10,
            "max_y": 10,
            "min_x": 0,
            "max_x": 10,
            "title_y": [
                {"10": "10 Kč"},
                {"29": "29 Kč"},
                {"49": "49 Kč"},
                {"69": "69 Kč"},
                {"89": "89 Kč"},
                {"109": "109 Kč"},
            ],
            "title_x": [{'0': '27 Oct'}, {'1': '05 Nov'}, {'2': '15 Nov'}, {'3': '25 Nov'}, {'4': '05 Dec'}, {'5': '15 Dec'}, {'6': '25 Dec'}, {'7': '04 Jan'}, {'8': '14 Jan'}, {'9': '24 Jan'}, {'10': '03 Feb'}]
        }
        self.assertEqual(exp_meta["title_y"], metadata["title_y"])
        self.assertEqual(exp_meta["title_x"], metadata["title_x"])
