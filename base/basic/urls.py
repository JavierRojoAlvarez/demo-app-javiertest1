from django.urls import path
from basic.views import (
    HomeTemplateView, ServicesTemplateView, ContactTemplateView,
    AboutTemplateView, TestTemplateView
)


urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home-template'),
    path(
        'services/', ServicesTemplateView.as_view(), name='services-template'
    ),
    path('contact/', ContactTemplateView.as_view(), name='contact-template'),
    path('about/', AboutTemplateView.as_view(), name='about-template'),
    path('test/', TestTemplateView.as_view(), name='test-template'),
]
