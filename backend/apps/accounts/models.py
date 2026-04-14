from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_USER = "user"
    ROLE_ADMIN = "admin"
    ROLE_CHOICES = [
        (ROLE_USER, "User"),
        (ROLE_ADMIN, "Admin"),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)

    class Meta:
        db_table = "accounts_user"

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN or self.is_staff
