from django.conf import settings
from django.test import TestCase
from model_bakery import baker

from ..models import Product
from ...categories.models import Category
from ...currencies.models import Currency
from .. import utils


class ProductUtilsTestCase(TestCase):
    fixtures = ['currencies.json', 'categories.json']

