from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView,
    RegisterView,
    AdminOnlyView,
    ManagerOrAdminView,
)

urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='auth_register'),
    path('api/admin-only/', AdminOnlyView.as_view(), name='admin_only'),
    path('api/manager-admin/', ManagerOrAdminView.as_view(), name='manager_admin'),
]