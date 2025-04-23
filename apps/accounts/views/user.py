from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from ..serializers import UserSerializer, ProfileSerializer
from ..utils.permissions import IsOwner
from ..services import UserService

class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_object(self):
        return self.request.user.profile
    
    def perform_update(self, serializer):
        profile_data = serializer.validated_data
        UserService.update_user_profile(self.request.user, **profile_data)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)