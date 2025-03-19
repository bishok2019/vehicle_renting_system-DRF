from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('visitor_app.urls')),
    path('accounts/', include('account.urls')),
    path('role/', include('role_app.urls')),
    path('department/', include('department.urls')),
    path('vehicle/', include('vehicle.urls')),
    path('rental/', include('rent_vehicle.urls')),

    path('auth/', include('rest_framework.urls')),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('redoc/', SpectacularRedocView.as_view(), name='redoc'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)