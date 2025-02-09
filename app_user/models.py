from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class AppUser(models.Model):
    usr_id = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    full_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.email