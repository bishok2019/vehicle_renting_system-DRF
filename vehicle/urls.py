from django.urls import path
from . import views

urlpatterns = [
    path('', views.VehicleListView.as_view(), name='vehicles-list'),
    path('create/', views.VehicleCreateView.as_view(), name='vehicles-create'),
    path('<slug:slug>/', views.VehicleUpdateView.as_view(), name='vehicles-update'),
    # path('<int:pk>/', views.VehicleUpdateView.as_view(), name='vehicles-update'),
]