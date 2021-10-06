from django.core.cache import cache
from django.db import models

from main.apps.categories import constants


class Category(models.Model):
    slug = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='categories/icons')
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    @staticmethod
    def get_bank_account() -> 'Category':
        """ Vrátí kategorii pro běžné bankovní účty. """
        obj = Category.get_category_dict().get('bank-accounts')
        if obj is None:
            raise Category.DoesNotExist()
        return obj

    @staticmethod
    def get_bond() -> 'Category':
        """ Vrátí kategorii pro dluhopisy. """
        obj = Category.get_category_dict().get('bonds')
        if obj is None:
            raise Category.DoesNotExist()
        return obj

    @staticmethod
    def get_building_saving() -> 'Category':
        """ Vrátí kategorii pro stavební spoření. """
        obj = Category.get_category_dict().get('building-savings')
        if obj is None:
            raise Category.DoesNotExist()
        return obj

    @staticmethod
    def get_commodity() -> 'Category':
        """ Vrátí kategorii pro komodity. """
        obj = Category.get_category_dict().get('commodities')
        if obj is None:
            raise Category.DoesNotExist()
        return obj

    @staticmethod
    def get_crypto() -> 'Category':
        """ Vrátí kategorii pro kryptoměny. """
        obj = Category.get_category_dict().get('cryptos')
        if obj is None:
            raise Category.DoesNotExist()
        return obj

    @staticmethod
    def get_pension_saving() -> 'Category':
        """ Vrátí kategorii pro penzijní spoření. """
        obj = Category.get_category_dict().get('pension-savings')
        if obj is None:
            raise Category.DoesNotExist()
        return obj

    @staticmethod
    def get_saving_account() -> 'Category':
        """ Vrátí kategorii pro spořící účty. """
        obj = Category.get_category_dict().get('saving-accounts')
        if obj is None:
            raise Category.DoesNotExist()
        return obj

    @staticmethod
    def get_share_etf() -> 'Category':
        """ Vrátí kategorii pro podílové listy/etf. """
        obj = Category.get_category_dict().get('share-etf')
        if obj is None:
            raise Category.DoesNotExist()
        return obj

    @staticmethod
    def get_stock() -> 'Category':
        """ Vrátí kategorii pro akcie. """
        obj = Category.get_category_dict().get('stocks')
        if obj is None:
            raise Category.DoesNotExist()
        return obj

    @staticmethod
    def get_term_account() -> 'Category':
        """ Vrátí kategorii pro terminované vklady. """
        obj = Category.get_category_dict().get('term-accounts')
        if obj is None:
            raise Category.DoesNotExist()
        return obj

    @staticmethod
    def get_property() -> 'Category':
        """ Vrátí kategorii pro nemovitosti. """
        obj = Category.get_category_dict().get('properties')
        if obj is None:
            raise Category.DoesNotExist()
        return obj

    @staticmethod
    def get_category_dict() -> dict:
        return cache.get_or_set('category-dict', Category.objects.all().in_bulk(), 3600)

    def is_bank_account(self):
        return self.slug == constants.BANK_ACCOUNT_SLUG

    def is_bond(self):
        return self.slug == constants.BOND_SLUG

    def is_building_saving(self):
        return self.slug == constants.BUILDING_SAVING_SLUG

    def is_commodity(self):
        return self.slug == constants.COMMODITY_SLUG

    def is_crypto(self):
        return self.slug == constants.CRYPTO_SLUG

    def is_pension_saving(self):
        return self.slug == constants.PENSION_SAVING_SLUG

    def is_saving_account(self):
        return self.slug == constants.SAVING_ACCOUNT_SLUG

    def is_share_etf(self):
        return self.slug == constants.SHARE_ETF_SLUG

    def is_stock(self):
        return self.slug == constants.STOCK_SLUG

    def is_term_account(self):
        return self.slug == constants.TERM_ACCOUNT_SLUG

    def is_property(self):
        return self.slug == constants.PROPERTY_SLUG

