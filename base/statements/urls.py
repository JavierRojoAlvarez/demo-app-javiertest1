from django.urls import path
from statements.views import StatementsTemplateView


urlpatterns = [
    path('statements/', StatementsTemplateView.as_view(), name='statements'),
]
