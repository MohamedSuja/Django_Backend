from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
import os
from ..serializers import UserRegistrationSerializer, LoginRequestSerializer, TokenResponseSerializer, RefreshTokenRequestSerializer, UserSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
import jwt, datetime
import uuid
from ..models import User
from ...utils.permissions import IsAdmin, IsStaff, IsCustomer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Access token payload (short-lived)
        access_token_payload = {
            "user_id": user.id,
            "email": user.email,
            "user_type": user.user_type,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            "iat": datetime.datetime.utcnow(),
            "token_type": "access",
            "jti": str(uuid.uuid4())
        }

        # Refresh token payload (long-lived)
        refresh_token_payload = {
            "user_id": user.id,
            "email": user.email,
            "user_type": user.user_type,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
            "iat": datetime.datetime.utcnow(),
            "token_type": "refresh",
            "jti": str(uuid.uuid4())
        }
        secret_key = os.getenv("SECRET_KEY", "").lower()
        # Generate tokens
        access_token = jwt.encode(access_token_payload, secret_key, algorithm="HS256")
        refresh_token = jwt.encode(refresh_token_payload, secret_key, algorithm="HS256")
        
        response = Response()

         # Set HTTP-only cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            expires=access_token_payload["exp"],
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            expires=refresh_token_payload["exp"],
        )

        response.data = TokenResponseSerializer({
            'access_token': access_token,
            'refresh_token': refresh_token,  # Same refresh token
            'access_token_expiration': access_token_payload['exp'],
            'user_type': user.user_type
        }).data
        return response


class LoginView(APIView):
    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        # Access token payload (short-lived)
        access_token_payload = {
            "user_id": user.id,
            "email": user.email,
            "user_type": user.user_type,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            "iat": datetime.datetime.utcnow(),
            "token_type": "access",
            "jti": str(uuid.uuid4())
        }

        # Refresh token payload (long-lived)
        refresh_token_payload = {
            "user_id": user.id,
            "email": user.email,
            "user_type": user.user_type,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
            "iat": datetime.datetime.utcnow(),
            "token_type": "refresh",
            "jti": str(uuid.uuid4())
        }

        secret_key = os.getenv("SECRET_KEY", "").lower()

        # Generate tokens
        access_token = jwt.encode(access_token_payload, secret_key, algorithm="HS256")

        refresh_token = jwt.encode(refresh_token_payload, secret_key, algorithm="HS256")

        response = Response()

        # Set HTTP-only cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            expires=access_token_payload["exp"],
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            expires=refresh_token_payload["exp"],
        )

        # Response data
        response.data = TokenResponseSerializer(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "access_token_expiration": access_token_payload["exp"],
                "user_type": user.user_type,
            }
        ).data

        return response
    


class TokenRefreshView(APIView):
     def post(self, request):
        # Validate refresh token from request body
        serializer = RefreshTokenRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        get_refresh_token = serializer.validated_data['refresh_token']
        

        secret_key = os.getenv("SECRET_KEY", "").lower()

        if not get_refresh_token:
            raise AuthenticationFailed('Refresh token missing!')
        
        try:
            payload = jwt.decode(get_refresh_token, secret_key, algorithms=['HS256'])
            
            if payload.get('token_type') != 'refresh':
                raise AuthenticationFailed('Invalid token type!')
                
            user = User.objects.filter(email=payload['email']).first()
            if user is None:
                raise AuthenticationFailed('User not found!')
                
            # Generate new access token
            access_token_payload = {
                "user_id": user.id,
                "email": user.email,
                "user_type": user.user_type,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
                'iat': datetime.datetime.utcnow(),
                'token_type': 'access',
                "jti": str(uuid.uuid4())
            }

            refresh_token_payload = {
                "user_id": user.id,
                "email": user.email,
                "user_type": user.user_type,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
                'iat': datetime.datetime.utcnow(),
                'token_type': 'refresh',
                "jti": str(uuid.uuid4())
            }
            
            access_token = jwt.encode(access_token_payload, secret_key, algorithm='HS256')
            refresh_token = jwt.encode(refresh_token_payload, secret_key, algorithm='HS256')
            
            response = Response()
            
            # Set HTTP-only cookies
            response.set_cookie(
                 key="access_token",
                 value=access_token,
                 httponly=True,
                 expires=access_token_payload["exp"],
                )
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
               expires=refresh_token_payload["exp"],
            )
            
            response.data = TokenResponseSerializer({
                'access_token': access_token,
                'refresh_token': refresh_token,  # Same refresh token
                'access_token_expiration': access_token_payload['exp'],
                'user_type': user.user_type
            }).data
            
            return response
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Refresh token expired!')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid refresh token!')


class UserView(APIView):  
    def get(self, request):
       
        token = request.COOKIES.get('access_token')

        if not token:
            return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            secret_key = os.getenv("SECRET_KEY", "").lower()
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            user = User.objects.get(email=payload["email"])
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired."}, status=status.HTTP_401_UNAUTHORIZED)
     
            
 
  