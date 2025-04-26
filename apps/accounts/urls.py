from django.urls import path
from .views import (
    LoginView,
    RegisterView,
    RefreshTokenView,
    UserProfileView,
    UserDetailView,
)

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('refresh', RefreshTokenView.as_view(), name='refresh'),
    path('user-detail', UserDetailView.as_view(), name='user-detail'),
    path('user-profile', UserProfileView.as_view(), name='user-profile'),
]