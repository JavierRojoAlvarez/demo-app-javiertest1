from django.http import HttpResponseRedirect
from my_app.ifrs16 import create_records
from my_app.calculate import calculate
from my_app.forms import TransactionFormSet


class CreateFormsetMixin:
    # formset_class = None
    form_initial_data = None
    formset_initial_data = None
    nested_data = None
    delete_transactions = True
    is_contract_view = False

    def post(self, request):
        self.object = None
        form = self.form_class(request.POST)
        formset = self.formset_class(request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
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
        return HttpResponseRedirect(
            self.request.POST.get('next', self.get_success_url())
        )

    def form_invalid(self, form, formset):
        print(form.errors, formset.errors)
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            context['form'] = self.form_class(
                initial=self.form_initial_data)
            formset = self.formset_class(initial=self.formset_initial_data)
            formset.extra = len(self.formset_initial_data)
            context['formset'] = formset
        print('Context delivered is:\n', context)
        return context


class UpdateFormsetMixin:
    # formset_class = None
    form_initial_data = None
    formset_initial_data = None
    nested_data = None
    delete_transactions = True
    is_contract_view = False

    def post(self, request):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        formset = self.formset_class(request.POST, instance=self.object)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
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
        return HttpResponseRedirect(
            self.request.POST.get('next', self.get_success_url())
        )

    def form_invalid(self, form, formset):
        print(form.errors, formset.errors)
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            print('Update view...', self.object)
            context['form'] = self.form_class(instance=self.object)
            formset = self.formset_class(instance=self.object)
            formset.extra = 0
            context['formset'] = formset
        print('Context delivered is:\n', context)
        return context
