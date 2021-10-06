import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager, CustomUserQuerySet


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(_('Email'), unique=True, max_length=128)
    phone = models.CharField(_('Phone'), blank=True, null=True, max_length=32)

    street = models.CharField(max_length=255)
    number = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=10)

    invoice_name = models.CharField(max_length=255)
    invoice_street = models.CharField(max_length=255)
    invoice_number = models.CharField(max_length=10)
    invoice_city = models.CharField(max_length=255)
    invoice_zip = models.CharField(max_length=10)
    vat_number = models.CharField(max_length=32)
    reg_number = models.CharField(max_length=32)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, help_text=_('Určuje možnost přístupu do administrace'))
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager.from_queryset(CustomUserQuerySet)()
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('Uživatel')
        verbose_name_plural = _('Uživatelé')
        ordering = ['last_name', 'first_name']

    def __str__(self):
        if self.first_name != '' or self.last_name != '':
            return str(self.first_name + ' ' + self.last_name)
        return self.email

    @staticmethod
    def get_address(street, number, zip_code, city):
        return "{} {} {} {}".format(street, number, zip_code, city)

    @property
    def address(self):
        return User.get_address(self.street, self.number, self.zip, self.city)

    @property
    def full_name(self):
        return str(self)

    @property
    def short_name(self):
        return str(self.last_name)
