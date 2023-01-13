from django.views.generic import TemplateView
from django.urls import reverse_lazy
from basic.mixins.views.general import GeneralMixin


class HomeTemplateView(GeneralMixin, TemplateView):
    template_name = 'basic/home.html'
    active_keys = ['home_template_active']


class TestTemplateView(TemplateView):
    template_name = 'basic/test.html'
    login_url = reverse_lazy('login')


class ServicesTemplateView(GeneralMixin, TemplateView):
    template_name = 'basic/services-template/services-template.html'
    active_keys = ['services_template_active']


class ContactTemplateView(GeneralMixin, TemplateView):
    template_name = 'basic/contact-template/contact-template.html'
    active_keys = ['contact_template_active', 'info_active']


class AboutTemplateView(GeneralMixin, TemplateView):
    template_name = 'basic/about-template/about-template.html'
    active_keys = ['about_template_active', 'info_active']
