from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.api import views

router = DefaultRouter()
router.register(r'users', views.AdminUserViewSet, basename='admin-users')

urlpatterns = [
    path('', include(router.urls)),

    # Профіль користувача
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),

    # JWT авторизація
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Реєстрація користувачів
    path('register/', views.RegisterView.as_view(), name='register'),
]
