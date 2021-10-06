from django.conf import settings
from dj_rest_auth.serializers import PasswordResetSerializer
from rest_framework import serializers

from dj_rest_auth.registration.serializers import RegisterSerializer

from .models import User
from . import methods
from ...libraries.functions import get_absolute_url
from ...libraries.serializers.mixins import DynamicFieldsMixin


class UserRegisterSerializer(RegisterSerializer):
    pass


class UserSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'street',
            'number',
            'city',
            'zip',
            'address',
            'invoice_name',
            'invoice_street',
            'invoice_number',
            'invoice_city',
            'invoice_zip',
            'vat_number',
            'reg_number',
            'email',
            'phone',
        ]
        read_only_fields = ('id', 'address')

    def validate_email(self, email):
        if email is None:
            return email
        if methods.is_user_exist(email, self.instance.pk if self.instance else None):
            raise serializers.ValidationError('User with this email is already registered.')
        return email

    def get_address(self):
        return User.get_address(self.validated_data.get("street"),
                                self.validated_data.get("number"),
                                self.validated_data.get("zip"),
                                self.validated_data.get("city"))


class CustomPasswordResetSerializer(PasswordResetSerializer):

    def get_email_options(self):

        return {
            'extra_email_context': {
                'absolute_url': get_absolute_url(),
                'admin_url': settings.BASE_URL,
            },
            'html_email_template_name': 'registration/emails/html_password_reset_email.html',
        }
