from django.contrib import admin

from main.apps.categories import utils as category_utils
from .models import PortfolioValue


@admin.register(PortfolioValue)
class PortfolioValueAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'category_name', 'institution_name', 'product_name', 'value', 'date']
    list_filter = ['portfolio__category', 'date', 'portfolio__currency']
    search_fields = ['portfolio__name', 'portfolio__institution__name', 'portfolio__product__name']

    def get_queryset(self, request):
        return super(PortfolioValueAdmin, self).get_queryset(request)\
            .select_related('portfolio__category', 'portfolio__institution', 'portfolio__product', 'portfolio')

    def name(self, obj):
        return obj.name

    def category_name(self, obj):
        return category_utils.get_category_name(obj.portfolio.category_id)

    def institution_name(self, obj):
        return obj.portfolio.institution.name if obj.portfolio.institution else ""

    def product_name(self, obj):
        return obj.portfolio.product.name if obj.portfolio.product else ""
