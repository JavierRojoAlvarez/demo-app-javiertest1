from django.urls import path
from api.views import TrackerAPI, ExampleAPI, Liability


urlpatterns = [
    path('line/', TrackerAPI.as_view(), name='tracker'),
    path('example/', ExampleAPI.as_view(), name='example-api'),
    path('liability/', Liability.as_view(), name='liability-api'),
]
