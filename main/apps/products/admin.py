from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'get_value', 'evaluation', 'active']
    list_filter = ['category', 'active']
    search_fields = ['name']

    def get_value(self, obj):
        return round(obj.value)

