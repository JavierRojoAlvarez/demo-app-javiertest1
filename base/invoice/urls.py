from django.urls import path
from invoice.views import preview_pdf, ReceivedInvoiceCreateView


urlpatterns = [
    path('preview/', preview_pdf, name='preview'),
    path(
        'create/<int:pk>/', ReceivedInvoiceCreateView.as_view(),
        name='invoice-create'
    ),
]
