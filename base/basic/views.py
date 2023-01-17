from django.views.generic import TemplateView
from basic.mixins.views.general import GeneralMixin


class HomeTemplateView(GeneralMixin, TemplateView):
    template_name = 'basic/home-template/home-template.html'
    active_keys = ['home_template_active']


class ServicesTemplateView(GeneralMixin, TemplateView):
    template_name = 'basic/services-template/services-template.html'
    active_keys = ['services_template_active']


class ContactTemplateView(GeneralMixin, TemplateView):
    template_name = 'basic/contact-template/contact-template.html'
    active_keys = ['contact_template_active', 'info_active']


class AboutTemplateView(GeneralMixin, TemplateView):
    template_name = 'basic/about-template/about-template.html'
    active_keys = ['about_template_active', 'info_active']


class TrackerTemplateView(GeneralMixin, TemplateView):
    template_name = 'basic/tracker-template/tracker-template.html'
