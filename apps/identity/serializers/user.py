from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserTypeField(serializers.Field):
    def to_representation(self, value):
        # Convert integer to string representation
        return dict(User.USER_TYPE_CHOICES).get(value, value)

    def to_internal_value(self, data):
        # Convert string to integer value
        reverse_choices = {v.lower(): k for k, v in User.USER_TYPE_CHOICES}
        try:
            return reverse_choices[data.lower()]
        except KeyError:
            raise serializers.ValidationError(
                f"Invalid user_type. Must be one of: {', '.join([choice[1] for choice in User.USER_TYPE_CHOICES])}"
            )

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    user_type = UserTypeField()

    class Meta:
        model = User
        fields = ( 'email', 'password', 'user_type')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type']
        )
        return user
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "user_type", "is_active", "username", "last_login", "created_date", "modified_date")
        read_only_fields = ('email', 'user_type')


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
class TokenResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    access_token_expiration = serializers.DateTimeField()
    user_type = UserTypeField()

class RefreshTokenRequestSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)