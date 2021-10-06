from django import forms

from main.apps.portfolio.models import Portfolio


class PortfolioAdminForm(forms.ModelForm):

    class Meta:
        model = Portfolio
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PortfolioAdminForm, self).__init__(*args, **kwargs)
        self.fields['value'].required = True
        self.fields['current_eval'].required = True
