from django.http import HttpResponseRedirect
from my_app.ifrs16 import create_ifrs16_records
from my_app.calculate import calculate
from my_app.forms import TransactionFormSet


class CreateFormsetMixin:

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
        self.instances = formset.save()
        self.create_additional_records()
        return HttpResponseRedirect(
            self.request.POST.get('next', self.get_success_url())
        )

    def form_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            formset = self.formset_class()
            context['formset'] = formset
        return context

    def create_additional_records(self):
        pass


class UpdateFormsetMixin:
    delete_transactions = True

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
        filter_dict = {formset.__class__.fk.name: formset.instance.id}
        qs_children = formset.model.objects.filter(**filter_dict)
        qs_children.delete()
        if self.delete_transactions:
            filter_dict = {'contract_id': self.object.id}
            qs_children = TransactionFormSet.model.objects.filter(
                **filter_dict)
            qs_children.delete()
        self.instances = formset.save()
        for record in uncommitted_list:
            record.save()
        self.create_additional_records()
        return HttpResponseRedirect(
            self.request.POST.get('next', self.get_success_url())
        )

    def form_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            context['form'] = self.form_class(instance=self.object)
            formset = self.formset_class(instance=self.object)
            formset.extra = 0
            context['formset'] = formset
        return context

    def create_additional_records(self):
        pass


class Ifrs16FormsetMixin:
    def create_additional_records(self):
        payment_list = [instance.amount for instance in self.instances]
        date_list = [instance.date for instance in self.instances]
        actual_list = [
            instance.actual_expected for instance in self.instances
        ]
        create_ifrs16_records(
            payments=payment_list, dates=date_list, func=calculate,
            actuals=actual_list, contract=self.object
        )
