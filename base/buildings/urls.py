from django.urls import path
from buildings.views import (
    BuildingCreateView, BuildingUpdateView, BuildingDeleteView,
    BuildingListView, BuildingDetailView
)


urlpatterns = [
    path('create/', BuildingCreateView.as_view(), name='building-create'),
    path('list/', BuildingListView.as_view(), name='building-list'),
    path(
          'detail/<int:pk>/', BuildingDetailView.as_view(),
          name='building-detail'
    ),
    path(
          'update/<int:pk>/', BuildingUpdateView.as_view(),
          name='building-update'
    ),
    path(
          'delete/<int:pk>/', BuildingDeleteView.as_view(),
          name='building-delete'
    ),
]
