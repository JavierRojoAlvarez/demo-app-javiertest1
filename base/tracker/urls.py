from django.urls import path
from tracker.views import TrackerTemplateView

urlpatterns = [
    path('covid-19/', TrackerTemplateView.as_view(), name='tracker-template')
]
