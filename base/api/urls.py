from django.urls import path
from api.views import TrackerAPIView, ExampleAPIView, LiabilityAPIView


urlpatterns = [
    path('line/', TrackerAPIView.as_view(), name='tracker'),
    path('example/', ExampleAPIView.as_view(), name='example-api'),
    path('liability/', LiabilityAPIView.as_view(), name='liability-api'),
]
