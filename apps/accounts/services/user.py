from django.contrib.auth import get_user_model
from ..models import Profile

User = get_user_model()

class UserService:
    @staticmethod
    def create_user_profile(user, **profile_data):
        profile = Profile.objects.create(user=user, **profile_data)
        return profile
    
    @staticmethod
    def update_user_profile(user, **profile_data):
        profile = user.profile
        for field, value in profile_data.items():
            setattr(profile, field, value)
        profile.save()
        return profile