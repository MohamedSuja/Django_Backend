from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

from ..serializers import LoginSerializer, RegisterSerializer
from ..services import AuthService

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        tokens = AuthService.get_tokens_for_user(user)
        
        return Response(tokens, status=status.HTTP_200_OK)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        tokens = AuthService.get_tokens_for_user(user)
        
        return Response(tokens, status=status.HTTP_201_CREATED)

class RefreshTokenView(TokenRefreshView):
    pass