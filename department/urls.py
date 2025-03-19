from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.DepartmentRegistrationView.as_view(), name='register-department' ),
    path('', views.GetDepartmentView.as_view(), name='get-department' ),
    path('<int:pk>', views.UpdateDepartmentView.as_view(), name='update-department' ),

]