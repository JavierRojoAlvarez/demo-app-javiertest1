from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class ActiveMixin:
    '''
    Add items to context dictionary with a value of active for chosen keys
    '''
    active_keys = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_keys = self.active_keys
        if active_keys:
            for key in active_keys:
                context[key] = 'active'
        return context


class LoginRequiredUrlMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')
