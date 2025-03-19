from django.urls import path
# from .views import PermissionCategoryListCreateView, PermissionCategoryDetailView
from . import role_views, views


urlpatterns = [
    path('create', role_views.CreateRoleView.as_view(), name='role-list-create'),
    path('', role_views.GetRoleView.as_view(), name='role-detail'),
    path('<int:pk>/', role_views.UpdateRoleView.as_view(), name='role-update'),

    path('permissioncategory/create', views.CreatePermissionCategoryView.as_view(), name='permissioncategory-create'),
    path('permissioncategory/', views.GetPermissionCategoryView.as_view(), name='permissioncategory-list'),
    path('permissioncategory/<int:pk>/', views.UpdatePermissionCategoryView.as_view(), name='permissioncategory-update'),
]