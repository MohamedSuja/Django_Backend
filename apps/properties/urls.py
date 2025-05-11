
from django.urls import path
from .views import SearchProperty
from ..identity.jwt.Middleware import JWTAuthMiddleware


urlpatterns = [
    path('/search', JWTAuthMiddleware(SearchProperty, allowed_roles=['staff']), name='search property'),

]