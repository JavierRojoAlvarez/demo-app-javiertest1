from decimal import Decimal, ROUND_HALF_UP
import simplejson as json
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.urls import reverse_lazy
from my_app.forms import (
    TransactionForm, EntryFormSet, ContractForm, ContractPaymentFormSet
)
from my_app.models import Contract, ContractType, Transaction, TransactionType
from my_app.mixins.views.formset import (
    CreateFormsetMixin, UpdateFormsetMixin, Ifrs16FormsetMixin
)
from buildings.models import Region
from basic.mixins.views.general import GeneralMixin


class TransactionCreateView(CreateFormsetMixin, GeneralMixin, CreateView):
    model = Transaction
    template_name = 'my_app/transaction/transaction-create.html'
    success_url = reverse_lazy('transaction-list')
    form_class = TransactionForm
    formset_class = EntryFormSet
    active_keys = ['transaction_active', 'transaction_create_active']


class TransactionUpdateView(UpdateFormsetMixin, GeneralMixin, UpdateView):
    model = Transaction
    context_object_name = 'record'
    form_class = TransactionForm
    formset_class = EntryFormSet
    template_name = 'my_app/transaction/transaction-update.html'
    active_keys = ['transaction_update_active']
    success_url = reverse_lazy('transaction-list')


def transaction_formset_view(request):
    form_class = TransactionType
    formset_class = EntryFormSet
    template_name = 'my_app/transaction/transaction-formset.html'
    if request.method == 'POST':
        payload = json.load(request)
        payload = {k: v for k, v in payload.items() if v is not None}
        print('Filtered payload is:', payload)
        formset = formset_class(payload['current_data'])
        formset.is_valid()
        formset_data = []
        for form in formset.forms:
            fields = form.cleaned_data.keys()
            form_data = {}
            for field in fields:
                field_data = form[field].data
                if field_data:
                    form_data[field] = field_data
            formset_data.append(form_data)
        print('Formset data is:\n', formset_data)
        new_data = formset_data
        if 'add_entry' in payload:
            new_data.append({})
        if 'parent_type' in payload:
            try:
                record_id = int(payload['parent_type'])
                new_data = list(
                    (
                        form_class.objects.get(pk=record_id)
                        .pseudoentry_set.values(
                            'direction', 'account', 'amount'
                        )
                    )
                )
            except Exception as exc:
                print(exc)
        if 'amount' in payload:
            try:
                amount = Decimal(payload['amount']).quantize(
                    Decimal('0.01'), ROUND_HALF_UP)
                if amount < 0:
                    raise ValueError('Negative amount')
                for record in new_data:
                    record['amount'] = amount
            except Exception as exc:
                print(exc)
        if 'remove_entry' in payload:
            try:
                remove_entry_index = int(payload['remove_entry'])
                del new_data[remove_entry_index]
            except Exception as exc:
                print(exc)
        context = {}
        formset_class.extra = len(new_data)
        formset = formset_class(initial=new_data)
        context['formset'] = formset
        context['payload'] = payload
        print('The context delivered is:\n', context)
        return render(
            request, template_name, context,
            content_type='application/xhtml+xml'
        )


class TransactionListView(GeneralMixin, ListView):
    model = Transaction
    context_object_name = 'qs'
    active_keys = ['transaction_active', 'transaction_list_active']
    template_name = 'my_app/transaction/transaction-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['region_list'] = Region.objects.all()
        context['sort_direction_list'] = {'Ascending': '', 'Descending': '-'}
        context['sort_by_list'] = {'NIA': 'nia', 'Region': 'region__name'}
        try:
            context['region_id'] = int(self.request.GET.get('region'))
        except Exception:
            context['region_id'] = None
        try:
            context['sort_by_val'] = self.request.GET.get('sort_by')
        except Exception:
            context['sort_by_val'] = None
        try:
            context['sort_direction_val'] = self.request.GET.get(
                'sort_direction')
        except Exception:
            context['sort_direction_id'] = None
        return context


class ContractListView(GeneralMixin, ListView):
    model = Contract
    context_object_name = 'qs'
    active_keys = ['contract_active', 'contract_list_active']
    template_name = 'my_app/contract/contract-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['revenue_expenditure_dict'] = {
            'R': 'Revenue', 'E': 'Expenditure'
        }
        context['contract_type_qs'] = ContractType.objects.all()
        context['sort_direction_list'] = {'Ascending': '', 'Descending': '-'}
        context['sort_by_list'] = {'NIA': 'nia', 'Region': 'region__name'}
        context['form'] = ContractForm
        print(context)
        return context


class ContractCreateView(
    Ifrs16FormsetMixin, CreateFormsetMixin, GeneralMixin, CreateView
):
    model = Contract
    template_name = 'my_app/contract/contract-create.html'
    active_keys = ['contract_active', 'contract_create_active']
    success_url = reverse_lazy('contract-list')
    form_class = ContractForm
    formset_class = ContractPaymentFormSet


class ContractUpdateView(
    Ifrs16FormsetMixin, UpdateFormsetMixin, GeneralMixin, UpdateView
):
    model = Contract
    template_name = 'my_app/contract/contract-update.html'
    active_keys = ['contract_active']
    success_url = reverse_lazy('contract-list')
    form_class = ContractForm
    formset_class = ContractPaymentFormSet
    formset_qs = True

    def get_success_url(self):
        contract_id = self.kwargs['pk']
        return reverse_lazy('contract-detail', kwargs={'pk': contract_id})


def contract_formset_view(request):
    form_class = TransactionType
    formset_class = ContractPaymentFormSet
    template_name = 'my_app/contract/contract-formset.html'
    if request.method == 'POST':
        payload = json.load(request)
        payload = {k: v for k, v in payload.items() if v is not None}
        print('Filtered payload is:', payload)
        formset = formset_class(payload['current_data'])
        formset.is_valid()
        formset_data = []
        for form in formset.forms:
            fields = form.cleaned_data.keys()
            form_data = {}
            for field in fields:
                field_data = form[field].data
                if field_data:
                    form_data[field] = field_data
            formset_data.append(form_data)
        print('Formset data is:\n', formset_data)
        new_data = formset_data
        if 'add_entry' in payload:
            new_data.append({})
        if 'parent_type' in payload:
            try:
                record_id = int(payload['parent_type'])
                new_data = list(
                    (
                        form_class.objects.get(pk=record_id)
                        .pseudoentry_set.values(
                            'direction', 'account', 'amount'
                        )
                    )
                )
            except Exception as exc:
                print(exc)
        if 'amount' in payload:
            try:
                amount = Decimal(payload['amount']).quantize(
                    Decimal('0.01'), ROUND_HALF_UP)
                if amount < 0:
                    raise ValueError('Negative amount')
                for record in new_data:
                    record['amount'] = amount
            except Exception as exc:
                print(exc)
        if 'remove_entry' in payload:
            try:
                remove_entry_index = int(payload['remove_entry'])
                del new_data[remove_entry_index]
            except Exception as exc:
                print(exc)
        context = {}
        formset_class.extra = len(new_data)
        print('Final new data is:\n', new_data)
        formset = formset_class(initial=new_data)
        context['formset'] = formset
        print('The context delivered is:\n', context)
        return render(
            request, template_name, context,
            content_type='application/xhtml+xml'
        )


class ContractDetailView(GeneralMixin, DetailView):
    model = Contract
    context_object_name = 'record'
    template_name = 'my_app/contract/contract-detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['id'] = self.object.id
        return context
