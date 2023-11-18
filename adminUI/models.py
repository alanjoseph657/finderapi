from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    usertype = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.username


