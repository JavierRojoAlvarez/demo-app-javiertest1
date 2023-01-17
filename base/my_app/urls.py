from django.urls import path
from my_app.views import (
     TransactionCreateView, TransactionListView, TransactionUpdateView,
     ContractCreateNewView, ContractListView, ContractUpdateView,
     ContractDetailView, transaction_formset_view, contract_formset_view
)

urlpatterns = [
    path(
          'transaction/create', TransactionCreateView.as_view(),
          name='transaction-create'
    ),
    path(
          'transaction/list', TransactionListView.as_view(),
          name='transaction-list'
    ),
    path(
          'transaction/update/<int:pk>/', TransactionUpdateView.as_view(),
          name='transaction-update'
    ),
    path(
          'transaction/formset', transaction_formset_view,
          name='transaction-formset'
    ),
    path(
          'contract/create', ContractCreateNewView.as_view(),
          name='contract-create'
    ),
    path(
          'contract/list', ContractListView.as_view(), name='contract-list'
    ),
    path(
          'contract/detail/<int:pk>/', ContractDetailView.as_view(),
          name='contract-detail'
    ),
    path(
          'contract/update/<int:pk>/', ContractUpdateView.as_view(),
          name='contract-update'
    ),
    path(
          'contract/formset', contract_formset_view, name='transaction-formset'
    ),
]
