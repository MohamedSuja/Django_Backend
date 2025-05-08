from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from ..serializers import UserSerializer, CustomTokenObtainPairSerializer

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class AdminOnlyView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if not self.request.user.is_admin():
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()
    
    def get(self, request):
        content = {'message': 'Admin only endpoint'}
        return Response(content)

class ManagerOrAdminView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if not (self.request.user.is_admin() or self.request.user.is_manager()):
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()
    
    def get(self, request):
        content = {'message': 'Manager or Admin only endpoint'}
        return Response(content)