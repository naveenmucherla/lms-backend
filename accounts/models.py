from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('STUDENT', 'Student'),
        ('MENTOR', 'Mentor'),
        ('ADMIN', 'Admin'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="STUDENT"
    )
    is_approved = models.BooleanField(default=True)
