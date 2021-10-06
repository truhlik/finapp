from rest_framework import serializers

from main.apps.categories.serializers import CategorySerializer
from main.apps.currencies.serializer import CurrencySerializer
from main.apps.currencies.models import Currency

from main.apps.institutions.serializers import InstitutionSerializer
from main.apps.institutions.models import Institution

from main.apps.products.serializers import ProductSerializer
from main.apps.products.models import Product
from main.libraries.serializers.fields import DecimalFloatField

from .. import utils


class BasePortfolioSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category_obj = CategorySerializer(read_only=True, source='category')
    product_obj = ProductSerializer(allow_null=True, read_only=True, source='product')
    currency_obj = CurrencySerializer(read_only=True, source='currency')
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.active(),
                                                    required=True,
                                                    source='product')  # todo active jen při create
    currency_id = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all(), required=True, source='currency')
    units = DecimalFloatField()

    class Meta:
        fields = [
            # read only fields
            'id',
            'category_obj',
            'product_obj',
            'currency_obj',
            # writable fields
            'name',
            'product_id',
            'currency_id',
            'units',
        ]
        read_only_fields = [
            'id',
            'category_obj',
            'product_obj',
            'currency_obj',
        ]

    def validate(self, attrs):
        product = attrs.get('product')
        currency = attrs.get('currency')

        if self.instance is not None:
            self.validate_on_update(attrs)

        if product and product.category != self.get_category():
            raise serializers.ValidationError({'product_id': 'Zvolený produkt není přiřazen k této kategorii portfolia.'})

        if product and currency and not product.currencies.filter(code=currency.code).exists():
            raise serializers.ValidationError({'currency_id': 'Zvolený produkt není dostupný ve zvolené měně.'})

        return attrs

    def validate_on_update(self, attrs):
        product = attrs.get('product')
        currency = attrs.get('currency')
        if product and self.instance.product != product:
            raise serializers.ValidationError({'product': 'Nemůžete změnit produkt.'})

        if currency and self.instance.currency != currency:
            raise serializers.ValidationError({'currency': 'Nemůžete změnit měnu.'})

    def create(self, validated_data):
        validated_data['category'] = self.get_category()
        validated_data['owner'] = self.get_owner()
        instance = super(BasePortfolioSerializer, self).create(validated_data)
        utils.create_initial_value_for_portfolio(instance)
        return instance

    def update(self, instance, validated_data):
        if validated_data['units'] != instance.units:
            instance.value = utils.get_value_for_portfolio(instance.product, validated_data['units'])
        return super(BasePortfolioSerializer, self).update(instance, validated_data)

    def get_category(self):
        raise NotImplementedError()

    def get_owner(self):
        return self.context['request'].user  # todo musim upravit pri vytvareni poradcem


class BaseWithInsitutionPortfolioSerializer(BasePortfolioSerializer):
    institution_obj = InstitutionSerializer(allow_null=True, read_only=True, source='institution')
    institution_id = serializers.PrimaryKeyRelatedField(queryset=Institution.objects.active(),
                                                        required=True,
                                                        source='institution')  # todo active jen při create

    class Meta:
        fields = BasePortfolioSerializer.Meta.fields + [
            'institution_obj',
            'institution_id',
        ]
        read_only_fields = BasePortfolioSerializer.Meta.read_only_fields + [
            'institution_obj',
        ]

    def validate(self, attrs):
        attrs = super(BaseWithInsitutionPortfolioSerializer, self).validate(attrs)

        institution = attrs.get('institution')
        product = attrs.get('product')

        if product and institution and not product.institutions.filter(id=institution.id).exists():
            raise serializers.ValidationError({'product_id': 'Zvolený produkt není přiřazen k této instituci.'})

        if institution and not institution.categories.filter(slug=self.get_category().slug).exists():
            raise serializers.ValidationError({'institution_id': 'Zvolená instituce není přiřazena k této kategorii portfolia.'})

        return attrs
