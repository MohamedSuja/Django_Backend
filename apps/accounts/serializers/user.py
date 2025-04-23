from rest_framework import serializers
from .auth import RegisterSerializer
from ..models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        from django.contrib.auth import get_user_model
        model = get_user_model()
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'is_active']
        read_only_fields = ['id', 'is_active']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['user', 'bio', 'phone', 'birth_date', 'avatar']
        read_only_fields = ['user']
    
    def update(self, instance, validated_data):
        # Handle avatar separately to avoid deletion when updating other fields
        if 'avatar' in validated_data:
            instance.avatar = validated_data['avatar']
        
        instance.bio = validated_data.get('bio', instance.bio)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        
        instance.save()
        return instance