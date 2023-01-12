from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy


class LoginRequiredUrlMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')


class TrackerTemplateView(LoginRequiredUrlMixin, TemplateView):
    template_name = 'tracker/tracker.html'
