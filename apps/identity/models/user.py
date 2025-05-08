from django.db import models
from django.contrib.auth.models import AbstractUser

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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'user_type' ]
    
    def __str__(self):
        return self.email