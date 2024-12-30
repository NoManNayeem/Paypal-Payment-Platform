from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add a role field to distinguish between user types
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('restaurant_owner', 'Restaurant Owner'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    # Add a branch field (only applicable for staff)
    branch = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
