from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.db.models import Count, Sum
from buildings.models import Region, Building
from buildings.forms import BuildingForm
from basic.mixins.views.general import GeneralMixin


class BuildingCreateView(GeneralMixin, CreateView):
    model = Building
    form_class = BuildingForm
    template_name = 'buildings/building-create/building-create.html'
    active_keys = ['asset_management_active', 'asset_management_create_active']
    success_url = reverse_lazy('building-list')


class BuildingListView(GeneralMixin, ListView):
    model = Building
    context_object_name = 'qs'
    active_keys = ['asset_management_active', 'asset_management_list_active']
    template_name = 'buildings/building-list/building-list.html'

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
    template_name = 'buildings/building-update/building-update.html'
    active_keys = ['occupation_update_active']

    def get_success_url(self):
        building_id = self.kwargs['pk']
        return reverse_lazy('building-detail', kwargs={'pk': building_id})


class BuildingDetailView(GeneralMixin, DetailView):
    model = Building
    context_object_name = 'record'
    template_name = 'buildings/building-detail/building-detail.html'


class BuildingDeleteView(GeneralMixin, DeleteView):
    model = Building
    context_object_name = 'record'
    template_name = 'buildings/building-delete/building-delete.html'
    success_url = reverse_lazy('building-list')
    login_url = reverse_lazy('login')
