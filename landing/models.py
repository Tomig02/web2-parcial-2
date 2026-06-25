from django.db import models

class UserMessages(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.EmailField(max_length=254) 
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} {self.surname}"