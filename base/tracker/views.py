from django.views.generic import TemplateView
from basic.views import LoginRequiredUrlMixin


class TrackerTemplateView(LoginRequiredUrlMixin, TemplateView):
    template_name = 'tracker/tracker.html'
