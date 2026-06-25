from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class AuthorizedUsers(models.Model):
    # Django automatically adds an 'id' auto-increment column
    name = models.CharField(max_length=200)
    email = models.EmailField()
    code = models.CharField(blank=True, null=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)