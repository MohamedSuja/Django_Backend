from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser, PermissionsMixin):
    ADMIN = 1
    MANAGER = 2
    EMPLOYEE = 3

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (EMPLOYEE, 'Employee')
    )
    
    email = models.EmailField(_('email address'), unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    
    def __str__(self):
        return self.email
    

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_manager(self):
        return self.role == self.MANAGER

    @property
    def is_employee(self):
        return self.role == self.EMPLOYEE