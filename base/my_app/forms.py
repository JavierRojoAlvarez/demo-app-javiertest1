from datetime import datetime
from django import forms
from django.forms import ModelForm
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from website.settings import DATE_INPUT_FORMATS
from cashflows.models import Cashflow
from .models import Entry, Transaction, ContractPayment, Contract


reg_attrs = {'class': 'form-control form-control-md rounded'}
check_attrs = {
    'class': 'form-control form-control-sm', 'style': 'width: 1.5rem;'
}
date_attrs = {
    'class': 'form-control form-control-md rounded date-input', 'name': 'date'
}
req_attrs = {'required': 'required'}
today = datetime.today().strftime('%d/%m/%Y')


class CashflowForm(ModelForm):
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


class EntryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Entry
        widgets = {
            'direction': forms.Select(attrs={**reg_attrs, **req_attrs}),
            'transaction': forms.Select(attrs={**reg_attrs, **req_attrs}),
            'account': forms.Select(attrs={**reg_attrs, **req_attrs}),
            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control form-control-md rounded amount',
                    'required': 'required'
                }
            ),
        }
        fields = list(widgets.keys())


class EntryContractForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Entry
        widgets = {
            'direction': forms.Select(attrs={**reg_attrs, **req_attrs}),
            'contract': forms.Select(attrs={**reg_attrs, **req_attrs}),
            'account': forms.Select(attrs={**reg_attrs, **req_attrs}),
            'amount': forms.NumberInput(
                attrs={'class': 'form-control form-control-md rounded amount'}
            ),
        }
        fields = list(widgets.keys())


class TransactionForm(ModelForm):
    def __init__(self, *args, initial_data=None, nested_data=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_data = initial_data
        self.nested_data = nested_data

    date = forms.DateField(
        initial=today,
        widget=forms.DateInput(
            format=DATE_INPUT_FORMATS[0], attrs=date_attrs
        ),
    )

    class Meta:
        model = Transaction
        widgets = {
            'transaction_type': forms.Select(attrs=reg_attrs),
            'contract': forms.Select(attrs=reg_attrs),
            'period': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-md rounded',
                    'placeholder': 'Period'
                }
            ),
            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control form-control-md rounded amount',
                    'placeholder': 'Amount'
                }
            ),
            'actual_expected': forms.Select(attrs=reg_attrs),

        }
        fields = list(widgets.keys())


class ContractPaymentForm(ModelForm):
    def __init__(self, *args, initial_data=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_data = initial_data

    date = forms.DateField(
        initial=today,
        widget=forms.DateInput(
            format=DATE_INPUT_FORMATS[0], attrs=date_attrs
        ),
    )

    class Meta:
        model = ContractPayment
        widgets = {
            'transaction_type': forms.Select(attrs=reg_attrs),
            'contract': forms.Select(attrs=reg_attrs),
            'period': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-md rounded',
                    'placeholder': 'Period'
                }
            ),
            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control form-control-md rounded amount',
                    'placeholder': 'Amount'
                }
            ),
            'actual_expected': forms.Select(attrs=reg_attrs)
        }
        fields = list(widgets.keys())


class ContractForm(ModelForm):
    sort_by_fields = ['start', 'end', 'organisation']
    filter_fields = [
        'revenue_expenditure', 'contract_type', 'organisation', 'start', 'end',
        'signed'
    ]
    filter_groups = [
        ['revenue_expenditure', 'contract_type'],
        ['organisation', 'signed'],
        ['building'],
    ]

    class Meta:
        model = Contract
        widgets = {
            'revenue_expenditure': forms.Select(attrs=reg_attrs),
            'contract_type': forms.Select(attrs=reg_attrs),
            'organisation': forms.Select(attrs=reg_attrs),
            'building': forms.SelectMultiple(
                attrs={
                    'class': (
                        'form-control form-control-md rounded selectpicker'
                    ),
                    'title': "Select any number of buildings",
                    'data-actions-box': "true", 'data-live-search': "true"
                }
            ),
            # 'treatment':forms.Select(attrs=reg_attrs),
            # 'start': forms.DateInput(
            # 	format=DATE_INPUT_FORMATS, attrs=date_attrs
            # ),
            # 'end': forms.DateInput(
            # 	format=DATE_INPUT_FORMATS, attrs=date_attrs
            # ),
            'description': forms.TextInput(attrs=reg_attrs),
            'signed': forms.CheckboxInput(attrs=check_attrs)
        }
        fields = list(widgets.keys())


class BaseEntryFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_form_kwargs(self, index):
        form_kwargs = super().get_form_kwargs(index)
        nested_data = form_kwargs['nested_data']
        if index < len(nested_data):
            form_kwargs['initial_data'] = nested_data[index]
        else:
            form_kwargs['initial_data'] = [
                {'direction': 1}, {'direction': 2}
            ]
        return form_kwargs

    def add_fields(self, form, index):
        super().add_fields(form, index)
        nested = EntryFormSet(
            data=form.data if form.is_bound else None,
            instance=form.instance,
            initial=form.initial_data,
            files=form.files if form.is_bound else None,
            prefix=f'entry-{form.prefix}-{EntryFormSet.get_default_prefix()}',
        )
        nested.extra = 2
        form.nested = nested

    def clean(self):
        """
        If a parent form has no data, but its nested forms do, we should
        return an error, because we can't save the parent.
        For example, if the TransactionForm is empty, but there are Entries.
        """
        for form in self.forms:
            if form.cleaned_data == {}:
                form.add_error(field=None, error='Form is empty. Please fill')

    def save(self, commit=True):
        result = super().save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result


EntryFormSet = inlineformset_factory(
    Transaction, Entry, form=EntryForm, can_delete=False
)
TransactionFormSet = inlineformset_factory(
    Contract, Transaction, form=TransactionForm, can_delete=False
)
ContractPaymentFormSet = inlineformset_factory(
    Contract, ContractPayment, form=ContractPaymentForm, can_delete=False
)
EntryContractFormSet = inlineformset_factory(
    Contract, Entry, form=EntryContractForm, can_delete=False
)
