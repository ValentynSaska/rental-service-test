from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

from apps.apartments.views import ApartmentListView, ApartmentDetailView, ApartmentDeleteView, ApartmentUpdateView
from config.settings import dev as settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('apps.users.api.urls')),
    
    path('api/v1/apartments/', ApartmentListView.as_view(), name='apartment-list'),
    path('api/v1/apartments/<slug:slug>/', ApartmentDetailView.as_view(), name='apartment-detail'),

    path('api/v1/apartments/<slug:slug>/delete/', ApartmentDeleteView.as_view(), name='apartment-delete'),
    path('api/v1/apartments/<slug:slug>/update/', ApartmentUpdateView.as_view(), name='apartment-update'),

    path('api/v1/bookings/', include('apps.booking.urls')),


    # Documentation
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
