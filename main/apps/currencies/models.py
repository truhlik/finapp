from django.db import models
from django.utils.translation import ugettext_lazy as _


class Currency(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('měna')
        verbose_name_plural = _('měny')

    def __str__(self):
        return self.name

    @staticmethod
    def get_czk():
        return Currency.objects.get(code='CZK')

    @staticmethod
    def get_eur():
        return Currency.objects.get(code='EUR')

    @staticmethod
    def get_usd():
        return Currency.objects.get(code='USD')
