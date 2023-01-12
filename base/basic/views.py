from django.views.generic import TemplateView
from django.urls import reverse_lazy
from basic.mixins.views.general import ActiveMixin, LoginRequiredUrlMixin


class HomeTemplateView(ActiveMixin, LoginRequiredUrlMixin, TemplateView):
    template_name = 'basic/home.html'
    active_keys = ['home_template_active']


class TestTemplateView(TemplateView):
    template_name = 'basic/test.html'
    login_url = reverse_lazy('login')


class ServicesTemplateView(ActiveMixin, LoginRequiredUrlMixin, TemplateView):
    template_name = 'basic/services.html'
    active_keys = ['services_template_active']


class ContactTemplateView(ActiveMixin, LoginRequiredUrlMixin, TemplateView):
    template_name = 'basic/contact.html'
    active_keys = ['contact_template_active', 'info_active']


class AboutTemplateView(ActiveMixin, LoginRequiredUrlMixin, TemplateView):
    template_name = 'basic/about.html'
    active_keys = ['about_template_active', 'info_active']
