from itertools import repeat
from decimal import Decimal, ROUND_HALF_UP
import datetime
import simplejson as json
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from my_app.forms import (
    TransactionForm, EntryFormSet, ContractForm,
    ContractPaymentFormSet, TransactionFormSet
)
from my_app.ifrs16 import create_records
from my_app.models import Contract, ContractType, Transaction, TransactionType
from my_app.calculate import calculate
from buildings.models import Region
from basic.mixins.views.general import GeneralMixin

today = datetime.date.today().strftime("%d/%m/%Y")


class FormsetMixin:
    # formset_class = None
    form_initial_data = None
    formset_initial_data = None
    nested_data = None
    is_update_view = False
    delete_transactions = True
    is_contract_view = False

    def post(self, request):
        if self.is_update_view:
            self.object = self.get_object()
            form = self.form_class(request.POST, instance=self.object)
            formset = self.formset_class(request.POST, instance=self.object)
        else:
            self.object = None
            form = self.form_class(request.POST)
            formset = self.formset_class(request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        if self.is_update_view:
            form.save()
            formset.instance = self.object
            uncommitted_list = []
            for form in formset:
                uncommitted_list.append(form.save(commit=False))
            print('LIST', uncommitted_list)
            filter_dict = {formset.__class__.fk.name: formset.instance.id}
            qs_children = formset.model.objects.filter(**filter_dict)
            qs_children.delete()
            print('Deleted queryset of children records')
            if self.delete_transactions:
                filter_dict = {'contract_id': self.object.id}
                qs_children = TransactionFormSet.model.objects.filter(
                    **filter_dict)
                qs_children.delete()
                print('Deleted old transaction records')
            formset.save()
            for record in uncommitted_list:
                print('Saving...', record)
                record.save()
            if self.is_contract_view:
                payment_list = [
                    form.cleaned_data['amount'] for form in formset
                ]
                date_list = [form.cleaned_data['date'] for form in formset]
                actual_list = [
                    form.cleaned_data['actual_expected'] for form in formset
                ]
                print('Actual list:', actual_list)
                create_records(
                    payments=payment_list, dates=date_list, func=calculate,
                    actuals=actual_list, contract=self.object
                )
        else:
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            if self.is_contract_view:
                payment_list = [
                    form.cleaned_data['amount'] for form in formset
                ]
                date_list = [form.cleaned_data['date'] for form in formset]
                actual_list = [
                    form.cleaned_data['actual_expected'] for form in formset
                ]
                print('Actual list:', actual_list)
                create_records(
                    payments=payment_list, dates=date_list, func=calculate,
                    actuals=actual_list, contract=self.object
                )
        if self.request.POST.get('next'):
            return HttpResponseRedirect(
                self.request.POST.get('next', self.get_success_url())
            )
        else:
            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        print(form.errors, formset.errors)
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            if self.is_update_view:
                print('Update view...', self.object)
                context['form'] = self.form_class(instance=self.object)
                formset = self.formset_class(instance=self.object)
                formset.extra = 0
                context['formset'] = formset
            else:
                context['form'] = self.form_class(
                    initial=self.form_initial_data)
                formset = self.formset_class(initial=self.formset_initial_data)
                formset.extra = len(self.formset_initial_data)
                context['formset'] = formset
        print('Context delivered is:\n', context)
        return context


class TransactionCreateView(FormsetMixin, GeneralMixin, CreateView):
    model = Transaction
    template_name = 'my_app/transaction/transaction-create.html'
    success_url = reverse_lazy('transaction-list')
    form_class = TransactionForm
    formset_class = EntryFormSet
    form_initial_data = {'date': today}
    formset_initial_data = [{'direction': 1}, {'direction': 2}]
    active_keys = ['transaction_active', 'transaction_create_active']


class TransactionUpdateView(FormsetMixin, GeneralMixin, UpdateView):
    model = Transaction
    context_object_name = 'record'
    form_class = TransactionForm
    formset_class = EntryFormSet
    formset_initial_data = [{'direction': 1}, {'direction': 2}]
    is_update_view = True
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


class ContractCreateNewView(FormsetMixin, GeneralMixin, CreateView):
    model = Contract
    template_name = 'my_app/contract/contract-create.html'
    active_keys = ['contract_active', 'contract_create_active']
    success_url = reverse_lazy('contract-list')
    form_class = ContractForm
    formset_class = ContractPaymentFormSet
    form_initial_data = {'start': today}
    formset_initial_data = []
    formset_initial_data.extend(repeat({'date': today}, 4))


class ContractUpdateView(FormsetMixin, GeneralMixin, UpdateView):
    model = Contract
    template_name = 'my_app/contract/contract-update.html'
    active_keys = ['contract_active']
    success_url = reverse_lazy('contract-list')
    form_class = ContractForm
    formset_class = ContractPaymentFormSet
    form_initial_data = {'start': today}
    formset_initial_data = []
    is_update_view = True
    formset_qs = True
    formset_initial_data.extend(repeat({'date': today}, 4))

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
