from model_bakery import baker
from rest_framework.test import APITestCase, APIRequestFactory, APIClient

from main.apps.currencies.models import Currency
from main.apps.products.models import Product


class JsonAPIClient(APIClient):

    def generic(self, method, path, data='', content_type='application/json', secure=False, **extra):
        return super().generic(method, path, data=data, content_type=content_type, secure=secure, **extra)

    def _encode_data(self, data, format='json', content_type=None):
        return super(JsonAPIClient, self)._encode_data(data, format='json', content_type=content_type)


class BaseTestCase(APITestCase):
    client_class = JsonAPIClient
    fixtures = ['currencies.json', 'categories.json']
    user = None
    maxDiff = None
    serializer_class = None
    model_class = None

    institution = None
    product = None

    def get_serializer_class(self):
        return self.serializer_class

    def get_model_class(self):
        return self.model_class

    def get_category_instance(self):
        raise NotImplementedError

    def get_user(self):
        if not self.user:
            self.user = baker.make('users.User')
        return self.user

    def get_currency(self):
        return Currency.get_czk()

    def do_auth(self):
        self.client.force_authenticate(user=self.get_user())

    def get_institution(self, with_category=True):
        if self.institution is not None:
            return self.institution

        if with_category:
            self.institution = baker.make('institutions.Institution', name='test', categories=[self.get_category_instance()])
        else:
            self.institution = baker.make('institutions.Institution', name='test')
        return self.institution

    def get_product(self, with_category=True, with_institution=True, with_currency=True):
        if self.product is not None:
            return self.product

        product = baker.make_recipe('main.apps.products.product', name='test', value=1)
        if with_category:
            product.category = self.get_category_instance()
        product.save()

        if with_institution:
            product.institutions.set([self.get_institution()])
        if with_currency:
            product.currencies.set([self.get_currency()])

        self.product = product
        return self.product

    def get_request_with_user(self):
        factory = APIRequestFactory()
        request = factory.get('/')
        self.do_auth()
        request.user = self.get_user()
        return request


