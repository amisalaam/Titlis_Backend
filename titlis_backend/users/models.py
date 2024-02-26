from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=250, unique=True)
    email = models.EmailField(max_length=250, unique=True)
    profile_image = models.ImageField(upload_to="profile", blank=True, null=True)
    profile_cover_image = models.ImageField(
        upload_to="profile_cover_image", blank=True, null=True
    )
    phone_number = PhoneNumberField(blank=True)
    is_google = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]