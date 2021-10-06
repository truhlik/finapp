import os
import csv
from django.conf import settings

from main.apps.categories.models import Category
from main.apps.currencies.models import Currency
from main.apps.institutions.models import Institution
from main.apps.products.models import Product


def create_product(category, name, value, currency, evaluation, company):

    currency_code_list = Currency.objects.all().values_list('code', flat=True)
    category_slug_list = Category.objects.all().values_list('slug', flat=True)

    # CATEGORY validation
    if category not in category_slug_list:
        print('Category {category} not in the supported list.'.format(category=category))
        return

    # NAME validation
    if name is None or name == "":
        print("Name is empty.")
        return

    # VALUE validation
    try:
        if value == "":
            value = float(1)
        else:
            value = value.replace(",", "")
            value = float(value)
    except ValueError:
        print('Value {value} not convertable.'.format(value=value))
        return

    # CURRENCY validation
    if currency not in currency_code_list:
        print('Currency {currency} not support'.format(currency=currency))
        return

    # EVALUATION validation
    try:
        evaluation = evaluation.replace("%", "").replace(" ", "").replace(",", ".")
        if evaluation == '':
            evaluation = float(3)
        else:
            evaluation = float(evaluation)
    except ValueError:
        print('Evaluation {evaluation} not convertable.'.format(evaluation=evaluation))
        return

    # bonds have value 1, but real value in data object
    data = {}
    if category == 'bonds':
        value = float(1)
        data['value'] = value

    _create_product(category, name, value, currency, evaluation, company, data)


def _create_product(category: str, name: str, value: float, currency: str, evaluation: float, company: str, data: dict):
    assert isinstance(category, str)
    assert isinstance(name, str)
    assert isinstance(value, (float, type(None),))
    assert isinstance(currency, str)
    assert isinstance(evaluation, (float, type(None),))
    assert isinstance(company, str)
    assert isinstance(data, dict)

    institution = None
    if company != "":
        institution, created = Institution.objects.get_or_create(name=company)
        institution.categories.add(category)

    try:
        product = Product.objects.get(
            category_id=category,
            name=name,
            institutions__name=company,
        )
    except Product.DoesNotExist:
        product = Product(
            category_id=category,
            name=name,
            active=True,
            evaluation=evaluation,
            value=value,
            data=data,
        )
        product.save()

        if institution:
            product.institutions.add(institution)

    currency = Currency.objects.get(code=currency)
    product.currencies.add(currency)


def seed_from_csv():
    with open(os.path.join(settings.BASE_DIR, 'seed', 'produkty.csv')) as f:
        r = csv.reader(f, delimiter=',')
        for row in r:
            create_product(
                category=row[0],
                name=row[1],
                value=row[2],
                currency=row[3],
                evaluation=row[4],
                company=row[5]
            )
