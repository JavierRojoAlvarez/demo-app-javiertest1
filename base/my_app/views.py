from itertools import repeat
from decimal import Decimal, ROUND_HALF_UP
import datetime
import simplejson as json
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db.models import Count, Sum
from django.urls import reverse_lazy
from my_app.forms import (
    TransactionForm, EntryFormSet, ContractForm, BuildingForm,
    ContractPaymentFormSet, TransactionFormSet
)
from my_app.ifrs16 import create_records
from my_app.models import (
    Contract, ContractType, Region, Building, Transaction, TransactionType
)
from my_app.calculate import calculate
from basic.mixins.views.general import GeneralMixin, LoginRequiredUrlMixin

today = datetime.date.today().strftime("%d/%m/%Y")


class FormsetMixin:
    # formset_class = None
    # formset_class2 = None
    form_initial_data = None
    formset_initial_data = None
    formset2_initial_data = None
    nested_data = None
    is_update_view = False
    formset_qs = False

    def post(self, request):
        if self.is_update_view:
            self.object = self.get_object()
            form = self.form_class(request.POST, instance=self.object)
            formset = self.formset_class(request.POST, instance=self.object)
        else:
            self.object = None
            form = self.form_class(request.POST)
            formset = self.formset_class(request.POST)
        if self.formset_class2:
            formset2 = self.formset_class2(request.POST)
            if form.is_valid() and formset.is_valid() and formset2.is_valid():
                return self.form_valid(form, formset, formset2=formset2)
            else:
                return self.form_invalid(form, formset, formset2=formset2)
        else:
            if form.is_valid() and formset.is_valid():
                return self.form_valid(form, formset)
            else:
                return self.form_invalid(form, formset)

    def form_valid(self, form, formset, formset2=None):
        if self.is_update_view:
            form.save()
            formset.instance = self.object
            filter_dict = {formset.__class__.fk.name: formset.instance.id}
            qs_child = formset.model.objects.filter(**filter_dict)
            qs_child.delete()
            formset.save()
        else:
            self.object = form.save()
            formset.instance = self.object
            formset.save()
        if formset2:
            formset2.instance = self.object
            formset2.save()
        if self.request.POST.get('next'):
            return HttpResponseRedirect(
                self.request.POST.get('next', self.get_success_url())
            )
        else:
            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset, formset2=None):
        return self.render_to_response(
            self.get_context_data(
                form=form, formset=formset, formset2=formset2)
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
                if self.formset_class2:
                    formset2 = self.formset_class2(
                        initial=self.formset2_initial_data)
                    formset2.extra = len(self.formset2_initial_data)
                    context['formset2'] = formset2
        print('Context delivered is:\n', context)
        return context


class FormsetNewMixin:
    # formset_class = None
    form_initial_data = None
    formset_initial_data = None
    nested_data = None
    is_update_view = False
    delete_transactions = True

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
            payment_list = [form.cleaned_data['amount'] for form in formset]
            date_list = [form.cleaned_data['date'] for form in formset]
            actual_list = [form.cleaned_data['actual_expected']
                           for form in formset]
            print('Actual list:', actual_list)
            create_records(
                payments=payment_list, dates=date_list, func=calculate,
                actuals=actual_list, contract=self.object
            )
        else:
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            payment_list = [form.cleaned_data['amount'] for form in formset]
            date_list = [form.cleaned_data['date'] for form in formset]
            actual_list = [form.cleaned_data['actual_expected']
                           for form in formset]
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


class TransactionUpdateView(FormsetNewMixin, GeneralMixin, UpdateView):
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


class ContractCreateNewView(FormsetNewMixin, GeneralMixin, CreateView):
    model = Contract
    template_name = 'my_app/contract/contract-create.html'
    active_keys = ['contract_active', 'contract_create_active']
    success_url = reverse_lazy('contract-list')
    form_class = ContractForm
    formset_class = ContractPaymentFormSet
    form_initial_data = {'start': today}
    formset_initial_data = []
    formset_initial_data.extend(repeat({'date': today}, 4))


class ContractUpdateView(FormsetNewMixin, GeneralMixin, UpdateView):
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


class BuildingCreateView(GeneralMixin, CreateView):
    model = Building
    form_class = BuildingForm
    template_name = 'my_app/building/building-create.html'
    active_keys = ['asset_management_active', 'asset_management_create_active']
    success_url = reverse_lazy('building-list')


class BuildingListView(GeneralMixin, ListView):
    model = Building
    context_object_name = 'qs'
    active_keys = ['asset_management_active', 'asset_management_list_active']
    template_name = 'my_app/building/building-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['summary'] = self.get_queryset().aggregate(
            Count('name'), Sum('nia'), Sum('ftes_capacity'))
        context['region_list'] = Region.objects.all()
        context['sort_direction_list'] = {'Ascending': '', 'Descending': '-'}
        context['sort_by_list'] = {'NIA': 'nia', 'Region': 'region__name'}
        return context

    def get_queryset(self):
        filter_list = ['region']
        name_list = ['region', 'sort_by', 'sort_direction']
        kwargs = {k: v for k, v in self.request.GET.items() if v}
        query_dict = {k: v for k, v in kwargs.items() if k in name_list}
        filter_dict = {k: int(v)
                       for k, v in query_dict.items() if k in filter_list}
        print('Query:'+str(query_dict))
        if query_dict:
            queryset = self.model.objects.filter(**filter_dict)
            if 'sort_direction' not in query_dict:
                query_dict['sort_direction'] = ''
            try:
                queryset = queryset.order_by(
                    query_dict['sort_direction']+query_dict['sort_by'])
            except Exception:
                pass
        else:
            queryset = self.model.objects.all()
        return queryset


class BuildingUpdateView(GeneralMixin, UpdateView):
    model = Building
    context_object_name = 'record'
    form_class = BuildingForm
    template_name = 'my_app/building/building-update.html'
    active_keys = ['occupation_update_active']

    def get_success_url(self):
        building_id = self.kwargs['pk']
        return reverse_lazy('building-detail', kwargs={'pk': building_id})


class BuildingDetailView(LoginRequiredUrlMixin, DetailView):
    model = Building
    context_object_name = 'record'
    template_name = 'my_app/building/building-detail.html'


class BuildingDeleteView(LoginRequiredUrlMixin, DeleteView):
    model = Building
    context_object_name = 'record'
    template_name = 'my_app/building/building-delete.html'
    success_url = reverse_lazy('building-list')
    login_url = reverse_lazy('login')
