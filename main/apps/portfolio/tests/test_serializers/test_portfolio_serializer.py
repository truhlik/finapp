from django.test import TestCase
from model_bakery import baker

from ...models import Portfolio
from ...serializers import PortfolioSerializer, AggregateValuesSerializer
from ....categories.models import Category
from ....currencies.models import Currency


class PortfolioSerializerTestCase(TestCase):
    fixtures = ['currencies.json', 'categories.json']
    maxDiff = None

    def test_values(self):
        institution = baker.make('institutions.Institution', name='test')
        product = baker.make_recipe('main.apps.products.product', name='test', currencies=[Currency.get_czk()])
        portfolio = baker.make(Portfolio,
                               name='test',
                               category=Category.get_bank_account(),
                               institution=institution,
                               product=product,
                               currency=Currency.get_czk(),
                               value=1,
                               current_eval=1)
        serializer = PortfolioSerializer(portfolio)
        exp_data = {
            'id': portfolio.id,
            'name': 'test',
            'category': {
                'slug': 'bank-accounts',
                'name': 'Běžné účty',
                'icon': 'http://example.com/media/categories/icons/bank-accounts.png',
            },
            'institution': {
                'id': institution.id,
                'name': 'test',
            },
            'product': {
                'id': product.id,
                'name': 'test',
                'currencies': [
                    {
                        'code': 'CZK',
                        'name': 'Kč'
                    }
                ],
                'evaluation': 3.0,
            },
            'currency': {
                'code': 'CZK',
                'name': 'Kč'
            },
            'value': 1,
            'current_eval': 1.0,
            'ytd_eval': None,
            'avg_eval': None,
            'total_eval': None,
            'weight_eval': None,
        }
        self.assertEqual(exp_data, serializer.data)


class AggregateValuesSerializerTestCase(TestCase):
    fixtures = ['currencies.json', 'categories.json']
    maxDiff = None

    def test_values(self):
        data = [
            {
                'category': 'bank-accounts',
                'name': 'Běžné účty',
                'current_eval': 5,
                'ytd_eval': None,
                'avg_eval': None,
                'total_eval': None,
                'weight_eval': None,
                'currency_code': 'CZK',
                'currency_name': 'Kč',
                'value': 5
            },
            {
                'category': 'properties',
                'name': 'Nemovitosti',
                'current_eval': 16,
                'ytd_eval': None,
                'avg_eval': None,
                'total_eval': None,
                'weight_eval': None,
                'currency_code': 'CZK',
                'currency_name': 'Kč',
                'value': 3
            }
        ]
        serializer = AggregateValuesSerializer(data)
        exp_data = {
            "sum_value": 8,
            "sum_evaluation": 9.12,
            "currency": {
                        'code': 'CZK',
                        'name': 'Kč'
                    },
            "results": [
                {
                    'portfolio_id': None,
                    'category': 'bank-accounts',
                    'name': 'Běžné účty',
                    'current_eval': 5.0,
                    'ytd_eval': None,
                    'avg_eval': None,
                    'total_eval': None,
                    'weight_eval': None,
                    'value': 5,
                    'currency': {
                        'code': 'CZK',
                        'name': 'Kč'
                    }
                },
                {
                    'portfolio_id': None,
                    'category': 'properties',
                    'name': 'Nemovitosti',
                    'current_eval': 16.0,
                    'ytd_eval': None,
                    'avg_eval': None,
                    'total_eval': None,
                    'weight_eval': None,
                    'value': 3,
                    'currency': {
                        'code': 'CZK',
                        'name': 'Kč'
                    }
                }
            ]

        }
        self.assertEqual(exp_data, dict(serializer.data))
