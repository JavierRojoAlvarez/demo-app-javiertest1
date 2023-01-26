from django import forms
from cashflows.models import Cashflow


reg_attrs = {'class': 'form-control form-control-md rounded'}


class CashflowForm(forms.ModelForm):
    class Meta:
        model = Cashflow
        widgets = {
            'category': forms.Select(attrs=reg_attrs),
            'building': forms.Select(attrs=reg_attrs),
            'value': forms.TextInput(attrs=reg_attrs),
            'start': forms.DateInput(attrs=reg_attrs),
            'end': forms.DateInput(attrs=reg_attrs),
        }
        fields = list(widgets.keys())
