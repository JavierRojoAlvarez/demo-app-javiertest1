from django.views.generic import TemplateView
from basic.mixins.views.general import LoginRequiredUrlMixin


class TrackerTemplateView(LoginRequiredUrlMixin, TemplateView):
    template_name = 'tracker/tracker.html'
