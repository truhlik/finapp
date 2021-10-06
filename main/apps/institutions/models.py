from django.db import models

from .managers import InstitutionQuerySet


class Institution(models.Model):
    objects = InstitutionQuerySet.as_manager()

    name = models.CharField(max_length=255)
    categories = models.ManyToManyField('categories.Category', related_name='institutions')
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'instituce'
        verbose_name_plural = 'instituce'

    def __str__(self):
        return self.name
