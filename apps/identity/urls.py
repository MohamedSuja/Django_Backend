from django.urls import path
from .views import RegisterView, LoginView, TokenRefreshView, UserView
from .jwt.Middleware import JWTAuthMiddleware


urlpatterns = [
    path('/register', RegisterView.as_view(), name='register'),
    path('/login', LoginView.as_view(), name='token_obtain_pair'),
    path('/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),


    path('/user', JWTAuthMiddleware(UserView.as_view(), allowed_roles=['admin']), name='user'),

]