from django.urls import path
from . import views

urlpatterns = [
    path('', views.RentVehicleView.as_view(), name='rent-vehicle'),
]
