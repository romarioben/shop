from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    "User derive from abstract User, we can add other field here if we want"
    email = models.EmailField(verbose_name='Email', unique=True)
    is_email_verified = models.BooleanField(default=False)
    