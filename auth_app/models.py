from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    "User derive from abstract User, we can add other field here if we want"
    ADMIN = 'admin'
    SELLER = 'seller'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (SELLER, 'Seller'),
    ]
    email = models.EmailField(verbose_name='Email', unique=True)
    is_email_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    receive_notifications = models.BooleanField(default=True)

    def is_admin(self):
        return self.role == self.ADMIN

    def is_seller(self):
        return self.role == self.SELLER
    