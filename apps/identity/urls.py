from django.urls import path
from .views import RegisterView, LoginView, TokenRefreshView, UserView


urlpatterns = [
    path('/register', RegisterView.as_view(), name='register'),
    path('/login', LoginView.as_view(), name='token_obtain_pair'),
    path('/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('/user', UserView.as_view(), name='user'),
]