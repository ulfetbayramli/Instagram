from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    # date_joined = models.DateTimeField(auto_now_add=True)
    # last_login = models.DateTimeField(null=True, blank=True)
    # profile_image = models.ImageField(upload_to='profile_images', null=True, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username']

    def __str__(self):
        return self.email  

    def save(self, *args, **kwargs):
        # Set username to email if it's blank
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
