from django.contrib import admin

from .forms import PortfolioAdminForm
from .models import Portfolio


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'category', 'institution', 'product', 'currency', 'get_units', 'get_value',
                    'current_eval']
    list_filter = ['category']
    search_fields = ['name']
    form = PortfolioAdminForm

    def get_queryset(self, request):
        return super(PortfolioAdmin, self).get_queryset(request).prefetch()

    def get_value(self, obj: Portfolio):
        return int(obj.value)

    def get_units(self, obj: Portfolio):
        return int(obj.units)


