from rest_framework import serializers

from .models import Category
from main.libraries.functions import get_absolute_url


class CategorySerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['slug', 'name', 'icon']
        read_only_fields = ['slug']

    def get_icon(self, obj):
        return get_absolute_url(obj.icon.url) if obj.icon else ''
