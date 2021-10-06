from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from main.apps.categories.models import Category
from main.apps.portfolio import managers
from main.apps.products.models import Product
from main.libraries.models import BaseModel


class Portfolio(BaseModel):
    objects = managers.PortfolioQuerySet.as_manager()

    owner = models.ForeignKey('users.User', related_name='portfolio', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.ForeignKey('categories.Category', related_name='portfolio', on_delete=models.CASCADE)
    institution = models.ForeignKey('institutions.Institution', blank=True, null=True, related_name='portfolio', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', related_name='portfolio', on_delete=models.CASCADE, blank=True, null=True)
    currency = models.ForeignKey('currencies.Currency', related_name='+', on_delete=models.CASCADE)
    units = models.DecimalField(decimal_places=12, max_digits=27)  # zadává uživatel jako vstup, jednotky, peníze atd.
    evaluation = models.DecimalField(decimal_places=2, max_digits=10)  # zadává uživatel jako denormalizovanonu hodnotu
    data = models.JSONField(encoder=DjangoJSONEncoder, default=dict)

    value = models.DecimalField(decimal_places=12, max_digits=27, blank=True)  # v setinách, vypočítává systém
    current_eval = models.DecimalField(decimal_places=2, max_digits=10, blank=True)  # v setinách procenta, vypočítává systém
    ytd_eval = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)  # v setinách procenta, vypočítává systém
    avg_eval = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)  # v setinách procenta, vypočítává systém
    total_eval = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)  # v setinách procenta, vypočítává systém
    weight_eval = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)  # v setinách procenta, vypočítává systém

    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'portfolio'
        verbose_name_plural = 'portfolio'

    def __str__(self):
        return self.name

    def clean(self):
        try:
            category = self.category
        except Category.DoesNotExist:
            category = None

        try:
            product = self.product
        except Product.DoesNotExist:
            product = None

        if self.institution and not self.institution.categories.filter(slug=self.category_id).exists():
            raise ValidationError({'institution': 'this institution does not belong to given category'})

        if product and self.product.category != category:
            raise ValidationError({'product': 'this product does not belong to given category'})

        if product and self.institution and not self.product.institutions.filter(id=self.institution_id).exists():
            raise ValidationError({'product': 'this product does not belong to given institution'})

        if product and not self.product.currencies.filter(code=self.currency_id).exists():
            raise ValidationError({'product': 'this product does not exist in given currency'})

    def set_data(self, key, value):
        if self.data:
            self.data[key] = value
        else:
            self.data = {key: value}

    def get(self, attr: str):
        return getattr(self, attr)

    def save(self, *args, **kwargs):
        if self.current_eval is None:
            self.current_eval = self.evaluation

        if self.value is None:
            self.value = 0  # ulozim si 0 docasne, protoze mi ji nekdo nastavi na spravnou hodnotu
        super(Portfolio, self).save(*args, **kwargs)
