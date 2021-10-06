import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(_('Vytvořeno'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Upraveno'), auto_now=True)

    class Meta:
        abstract = True


class SimpleModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('Vytvořeno'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Upraveno'), auto_now=True)

    class Meta:
        abstract = True
