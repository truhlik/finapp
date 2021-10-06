from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import ProductQuerySet


class Product(models.Model):
    objects = ProductQuerySet.as_manager()
    name = models.CharField(max_length=255)
    institutions = models.ManyToManyField('institutions.Institution', blank=True, related_name='products')
    currencies = models.ManyToManyField('currencies.Currency', blank=True, related_name='+')
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE, related_name='products')
    active = models.BooleanField(default=True)
    evaluation = models.DecimalField(decimal_places=2, max_digits=10)
    value = models.DecimalField(decimal_places=12, max_digits=27)
    data = models.JSONField(default=dict, encoder=DjangoJSONEncoder)
    order = models.PositiveBigIntegerField(blank=True, null=False)

    class Meta:
        verbose_name = _('produkt')
        verbose_name_plural = _('produkty')
        ordering = ('order', 'name')

    def __str__(self):
        return self.name

    # todo tohle musí být na formu, protože je to M2M vazba
    # def clean(self):
        # zkontroluju, že instituce přiřazené tomuto produktu mají odpovídající kategorii
        # if self.category_id and self.institutions.filter(categories=self.category).count() != self.institutions.all().count():
        #     raise ValidationError('One of given institution doesnt have same category')

    def save(self, *args, **kwargs):
        if self.order is None:
            qs = Product.objects.filter(category=self.category)
            if self.id is not None:
                qs = qs.exclude(id=self.id)
            self.order = qs.aggregate(max_order=models.Max('order')).get('max_order') or 0
        super(Product, self).save(*args, **kwargs)
