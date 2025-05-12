# middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

class JWTAuthMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None, allowed_roles=None):
        self.get_response = get_response
        self.allowed_roles = allowed_roles or []
        super().__init__(get_response)


    def process_request(self, request):
        # Skip auth for certain endpoints
        OPEN_ENDPOINTS = [
            '',
            '/admin',
            '__debug__',
            '/api/v1/auth/login',
            '/api/v1/auth/register',
        ]
    
        if request.path_info in OPEN_ENDPOINTS:
            return None
            
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header:
            return JsonResponse({'error': 'Authorization header missing'}, status=401)
            
        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
            # Validate token structure
            if payload.get('token_type') != 'access':
                raise jwt.InvalidTokenError('Invalid token type')
            


         
            # Check if user has required role
            user_type = self.get_user_type_string(payload['user_type'])
           
            roles = ['admin', 'customer', 'staff']  # Define your roles here
            if user_type not in roles:
                return JsonResponse(
                    {'error': f'Access restricted to {", ".join(roles)}'},
                    status=403
                )
            if self.allowed_roles and user_type not in self.allowed_roles:
                return JsonResponse(
                    {'error': f'Access restricted to {", ".join(self.allowed_roles)}'},
                    status=403
                )
                
            # Set user attributes from token
            request.user_id = payload['user_id']
            request.user_type = user_type
            
        except (IndexError, jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            return JsonResponse({'error': str(e)}, status=401)
            
        return None
    
    
    def get_user_type_string(self, user_type_int):
        """Convert integer user_type to its string representation using USER_TYPE_CHOICES"""
        if not hasattr(self, '_type_mapping'):
            # Create mapping only once
            User = get_user_model()
            self._type_mapping = dict(User.USER_TYPE_CHOICES)
        
        # Get string representation or return original if not found
        return self._type_mapping.get(user_type_int, str(user_type_int)).lower()