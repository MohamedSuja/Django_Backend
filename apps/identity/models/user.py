from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    CUSTOMER = 1
    STAFF = 2
    ADMIN = 3
    
    USER_TYPE_CHOICES = (
        (CUSTOMER, 'Customer'),
        (STAFF, 'Staff'),
        (ADMIN, 'Admin'),
    )
    
    
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=CUSTOMER)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    created_by = models.EmailField()
    modified_by = models.EmailField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'user_type' ]
    
    def __str__(self):
        return self.email